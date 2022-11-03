import os
import secrets
import Image
from ecommerce import app
from ecommerce.forms import *
from plotly.offline import plot
import plotly.graph_objs as go
from flask import Markup, flash
from ecommerce.models import *
from flask import Flask, Response, render_template, request
import json
import requests
import yaml
import razorpay
from flask import jsonify
import time

loadapi = yaml.safe_load(open('config.yaml'))
payapi = yaml.safe_load(open('api.yaml'))

rz_api = payapi['api_id']
rz_key = payapi['api_key']
client = razorpay.Client(auth=(rz_api, rz_key)) 

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    products = getProductList()
    products = [value for (value,) in products]
    return Response(json.dumps(products), mimetype='application/json')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            if isUserAdmin():
                # Return to admin page
                return redirect('admin')
            return redirect(url_for('root'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('index.html', error=error)


@app.route("/logout")
def logout():
    session.pop('email', None)
    session.pop('firstname', None)
    return redirect(url_for('root'))


@app.route("/registerationForm")
def registrationForm():
    return render_template("register.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Parse form data
        msg = extractAndPersistUserDataFromForm(request)
        if msg:
            # return render_template('index.html', error=msg)
            flash('Registered Successfully', 'success')
            return redirect(url_for('root'))
        else:
            return render_template('index.html', error="Registration failed")


@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def root():
    loggedIn, firstName, productCountinKartForGivenUser = getLoginUserDetails()
    session['firstname'] = firstName
    bidding_api_url = loadapi['biddingEngineUrl'] + '/auction_products'
    
    response = requests.get(bidding_api_url)
    prod_json = response.json()
    #print(prod_json)
    bidProductsDetails = getRecommendedProducts(prod_json)
    bidProductsMassagedDetails = massageItemData(bidProductsDetails)
    
    #allProductDetails = getAllProducts()
    #allProductsMassagedDetails = massageItemData(allProductDetails)
    categoryData = getCategoryDetails()

    if loggedIn:
        userid = getUserId()
        user_api_url = loadapi['userProductRecommendationServiceUrl']
        userid = {"userid": userid}
        response = requests.post(user_api_url, json=userid)
        prod_json = response.json()

        list = []
        for i in range(0, len(prod_json['Product_ids'])):
            list.append(prod_json['Product_ids'][i])

        recommendedProducts = getRecommendedProducts(list)
        recommendedProductsMassagedDetails = massageItemData(recommendedProducts)
        return render_template('index.html', itemData=bidProductsMassagedDetails, loggedIn=loggedIn,
                               firstName=firstName,
                               productCountinKartForGivenUser=productCountinKartForGivenUser,
                               categoryData=categoryData, recommendedProducts=recommendedProductsMassagedDetails)
    else:
        return render_template('index.html', itemData=bidProductsMassagedDetails, loggedIn=loggedIn,
                               firstName=firstName,
                               productCountinKartForGivenUser=productCountinKartForGivenUser,
                               categoryData=categoryData)


@app.route("/displayCategory")
def displayCategory():
    loggedIn, firstName, noOfItems = getLoginUserDetails()
    categoryId = request.args.get("categoryId")
    productDetailsByCategoryId = Product.query.join(ProductCategory, Product.productid == ProductCategory.productid) \
        .add_columns(Product.productid, Product.product_name, Product.regular_price, Product.discounted_price,
                     Product.image) \
        .join(Category, Category.categoryid == ProductCategory.categoryid) \
        .filter(Category.categoryid == int(categoryId)) \
        .add_columns(Category.category_name) \
        .all()

    categoryName = productDetailsByCategoryId[0].category_name
    data = massageItemData(productDetailsByCategoryId)
    return render_template('displayCategory.html', data=data, loggedIn=loggedIn, firstName=firstName,
                           noOfItems=noOfItems, categoryName=categoryName)



@app.route("/productDescription")
def productDescription():
    loggedIn, firstName, noOfItems = getLoginUserDetails()
    productid = request.args.get('productId')
    productDetailsByProductId = getProductDetails(productid)

    # get auction Information
    api_url = loadapi['biddingEngineUrl'] + '/auction'
    params = {"productId": productid}
    response = requests.get(api_url, params=params)
    response_json = response.json()
    auction_info = dict(response_json)
    #print(auction_info)
    biddableProduct = True if 'status' in auction_info and auction_info['status'] == 'open' else False
    #print(auction_info)
    
    # get recommended Items
    api_url = loadapi['recommendationServiceUrl']
    products = {"product_id": productid}
    response = requests.post(api_url, json=products)
    #print(response.text)
    prod_json = response.json()
    # prod_json = {"Product_ids": [202228337, 2, 3, 4, 5]}
    list = []
    for i in range(0, len(prod_json['Product_ids'])):
        list.append(prod_json['Product_ids'][i])

    recommendedProducts = getRecommendedProducts(list)
    recommendedProductsMassagedDetails = massageItemData(recommendedProducts)
    print(type(productDetailsByProductId))

    return render_template("productDescription.html", data=productDetailsByProductId, loggedIn=loggedIn,
                           firstName=firstName, productCountinKartForGivenUser=noOfItems,
                           recommendedProducts=recommendedProductsMassagedDetails,
                           biddableProduct = biddableProduct,
                           auctionDetails = auction_info,
                           biddingEngineUrl = loadapi['biddingEngineUrl'] + '/create_bid'
                           )


@app.route('/search', methods=['GET', 'POST'])
def index():
    loggedIn, firstName, productCountinKartForGivenUser = getLoginUserDetails()
    productName = request.args.get('productname')
    if productName == '':
        return redirect(url_for('root'))
    else:
        productDetailsByProductId = getProductDetailsByName(productName)
        if len(productDetailsByProductId) == 0:
            flash('No Products Found')
            return redirect(url_for('root'))
        else:
            id = productDetailsByProductId[0].productid
            api_url = loadapi['recommendationServiceUrl']
            products = {"product_id": id}
            response = requests.post(api_url, json=products)
            prod_json = response.json()
            list = []
            for i in range(0, len(prod_json['Product_ids'])):
                list.append(prod_json['Product_ids'][i])

            recommendedProducts = getRecommendedProducts(list)
            recommendedProductsMassagedDetails = massageItemData(recommendedProducts)
            return render_template("ProductSearch.html", itemData=productDetailsByProductId, loggedIn=loggedIn,
                                   firstName=firstName, productCountinKartForGivenUser=productCountinKartForGivenUser,
                                   recommendedProducts=recommendedProductsMassagedDetails)


@app.route("/addToCart", methods=['GET', 'POST'])
def addToCart():
    if isUserLoggedIn():
        product_details = request.form['weight']
        print(product_details)
        sku = product_details.split(" - ")[0]
        subproductId = product_details.split(" - ")[1]
        # Using Flask-SQLAlchmy SubQuery
        extractAndPersistKartDetailsUsingSubquery(sku, subproductId)
        # Using Flask-SQLAlchmy normal query
        # extractAndPersistKartDetailsUsingkwargs(productId)
        flash('Item successfully added to cart !!', 'success')
        return redirect(url_for('root'))
    else:
        flash('please log in !!', 'success')
        return redirect(url_for('root'))


@app.route("/addToCartProduct", methods=['GET', 'POST'])
def addToCartProduct():
    if isUserLoggedIn():
        productId = request.args.get('productId')
        subProductId = request.args.get('subProductId')
        print(session)
        extractAndPersistKartDetails(productId, subProductId)
        # Using Flask-SQLAlchmy normal query
        # extractAndPersistKartDetailsUsingkwargs(productId)
        flash('Item successfully added to cart !!', 'success')
        return redirect(url_for('root'))
    else:
        flash('please log in !!', 'success')
        return redirect(url_for('root'))


@app.route("/cart")
def cart():
    if isUserLoggedIn():
        loggedIn, firstName, productCountinKartForGivenUser = getLoginUserDetails()
        cartdetails, totalsum, tax = getusercartdetails()
        
        if cartdetails.count() > 0:
            products = {"product_id": cartdetails[0].productid}
        else: # default 
            products = {"product_id": 202212001}

        api_url = loadapi['recommendationServiceUrl']
        response = requests.post(api_url, json=products)
        #print(response.json())
        prod_json = response.json()
        # prod_json = {"Product_ids": [202228337, 2, 3, 4, 5]}
        # print(response.json())
        list = []
        for i in range(0, len(prod_json['Product_ids'])):
            list.append(prod_json['Product_ids'][i])

        recommendedProducts = getRecommendedProducts(list)
        recommendedProductsMassagedDetails = massageItemData(recommendedProducts)
        return render_template("cart.html", cartData=cartdetails,
                               productCountinKartForGivenUser=productCountinKartForGivenUser, loggedIn=loggedIn,
                               firstName=firstName, totalsum=totalsum, tax=tax,
                               recommendedProducts=recommendedProductsMassagedDetails)
    else:
        return redirect(url_for('root'))


@app.route("/admin/category/<int:category_id>", methods=['GET'])
def category(category_id):
    if isUserAdmin():
        category = Category.query.get_or_404(category_id)
        return render_template('adminCategory.html', category=category)
    return redirect(url_for('root'))


@app.route("/admin/categories/new", methods=['GET', 'POST'])
def addCategory():
    if isUserAdmin():
        form = addCategoryForm()
        if form.validate_on_submit():
            category = Category(category_name=form.category_name.data)
            db.session.add(category)
            db.session.commit()
            flash(f'Category {form.category_name.data}! added successfully', 'success')
            return redirect(url_for('getCategories'))
        return render_template("addCategory.html", form=form)
    return redirect(url_for('getCategories'))


@app.route("/admin/categories/<int:category_id>/update", methods=['GET', 'POST'])
def update_category(category_id):
    if isUserAdmin():
        category = Category.query.get_or_404(category_id)
        form = addCategoryForm()
        if form.validate_on_submit():
            category.category_name = form.category_name.data
            db.session.commit()
            flash('This category has been updated!', 'success')
            return redirect(url_for('getCategories'))
        elif request.method == 'GET':
            form.category_name.data = category.category_name
        return render_template('addCategory.html', legend="Update Category", form=form)
    return redirect(url_for('getCategories'))


@app.route("/admin/category/<int:category_id>/delete", methods=['POST'])
def delete_category(category_id):
    if isUserAdmin():
        ProductCategory.query.filter_by(categoryid=category_id).delete()
        db.session.commit()
        category = Category.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        flash('Your category has been deleted!', 'success')
    return redirect(url_for('getCategories'))


@app.route("/admin/categories", methods=['GET'])
def getCategories():
    if isUserAdmin():
        # categories = Category.query.all()
        cur = mysql.connection.cursor()
        # Query for number of products on a category:
        cur.execute(
            'SELECT category.categoryid, category.category_name, COUNT(product_category.productid) as noOfProducts FROM category LEFT JOIN product_category ON category.categoryid = product_category.categoryid GROUP BY category.categoryid');
        categories = cur.fetchall()
        return render_template('adminCategories.html', categories=categories)
    return redirect(url_for('root'))


# this method is copied from Schafer's tutorials
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/uploads', picture_fn)

    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/admin", methods=['GET'])
def admin():
    return render_template('admin.html')


@app.route("/admin/products", methods=['GET'])
def getProducts():
    if isUserAdmin():
        products = Product.query.order_by(Product.sku, Product.sub_product_id).all()
        return render_template('adminProducts.html', products=products)
    return redirect(url_for('root'))


@app.route("/admin/products/new", methods=['GET', 'POST'])
def addProduct():
    if isUserAdmin():
        form = addProductForm()
        form.category.choices = [(row.categoryid, row.category_name) for row in Category.query.all()]
        product_icon = ""  # safer way in case the image is not included in the form
        if form.validate_on_submit():
            if form.image.data:
                product_icon = save_picture(form.image.data)
            product = Product(sku=form.sku.data, product_name=form.productName.data,
                              description=form.productDescription.data, image=product_icon,
                              stock=form.productQuantity.data,
                              discounted_price=form.productPrice.data - (form.productPrice.data / 15), product_rating=0,
                              product_review=" ", regular_price=form.productPrice.data,
                              sub_product_id=form.subProductId.data, weight=form.weight.data, brand=form.brand.data)

            db.session.add(product)
            db.session.commit()
            product_category = ProductCategory(categoryid=form.category.data, productid=product.productid)
            db.session.add(product_category)
            db.session.commit()
            flash(f'Product {form.productName} added successfully', 'success')
            return render_template("admin.html")
        return render_template("addProduct.html", form=form, legend="New Product")
    return redirect(url_for('root'))


@app.route("/admin/product/<int:product_id>", methods=['GET'])
def product(product_id):
    if isUserAdmin():
        product = Product.query.get_or_404(product_id)
        return render_template('adminProduct.html', product=product)
    return redirect(url_for('root'))


@app.route("/admin/product/<int:product_id>/update", methods=['GET', 'POST'])
def update_product(product_id):
    if isUserAdmin():
        product = Product.query.get_or_404(product_id)
        form = addProductForm()
        form.category.choices = [(row.categoryid, row.category_name) for row in Category.query.all()]
        if form.validate_on_submit():
            if form.image.data:
                product.image = save_picture(form.image.data)
            product.product_name = form.productName.data
            product.sku = form.sku.data
            product.productDescription = form.productDescription.data
            product.stock = form.productQuantity.data
            # product.discounted_price = form.data.discounted_price = 15
            product.regular_price = form.productPrice.data
            db.session.commit()
            product_category = ProductCategory.query.filter_by(productid=product.productid).first()
            if form.category.data != product_category.categoryid:
                new_product_category = ProductCategory(categoryid=form.category.data, productid=product.productid)
                db.session.add(new_product_category)
                db.session.commit()
                db.session.delete(product_category)
                db.session.commit()

            flash('This product has been updated!', 'success')
            return redirect(url_for('getProducts'))
        elif request.method == 'GET':
            form.productName.data = product.product_name
            form.sku.data = product.sku
            form.productDescription.data = product.description
            form.productPrice.data = product.regular_price
            form.productQuantity.data = product.stock
        return render_template('addProduct.html', legend="Update Product", form=form)
    return redirect(url_for('root'))


@app.route("/admin/product/<int:product_id>/delete", methods=['POST'])
def delete_product(product_id):
    if isUserAdmin():
        product_category = ProductCategory.query.filter_by(productid=product_id).first()
        if product_category is not None:
            db.session.delete(product_category)
            db.session.commit()
        Cart.query.filter_by(productid=product_id).delete()
        db.session.commit()
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        flash('Your product has been deleted!', 'success')
    return redirect(url_for('getProducts'))


@app.route("/admin/users", methods=['GET'])
def getUsers():
    if isUserAdmin():
        # users = User.query.all()
        print('in')
        cur = mysql.connection.cursor()
        cur.execute(
            'SELECT u.fname, u.lname, u.email, u.active, u.city, u.state, COUNT(o.orderid) as noOfOrders FROM `user` u LEFT JOIN `order` o ON u.userid = o.userid GROUP BY u.userid')
        users = cur.fetchall()
        return render_template('adminUsers.html', users=users)
    return redirect(url_for('root'))


@app.route("/removeFromCart")
def removeFromCart():
    if isUserLoggedIn():
        productId = int(request.args.get('productId'))
        removeProductFromCart(productId)
        return redirect(url_for('cart'))
    else:
        return redirect(url_for('loginForm'))


@app.route("/checkoutPage")
def checkoutForm():
    if isUserLoggedIn():
        cartdetails, totalsum, tax = getusercartdetails()
        loggedIn, firstName, productCountinKartForGivenUser = getLoginUserDetails()
        return render_template("checkoutPage.html", cartData=cartdetails, totalsum=totalsum, tax=tax,
                                productCountinKartForGivenUser=productCountinKartForGivenUser, loggedIn=loggedIn,
                               firstName=firstName)
    else:
        return redirect(url_for('loginForm'))

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    loggedIn, firstName, productCountinKartForGivenUser = getLoginUserDetails()
    return render_template('404.html', loggedIn=loggedIn, firstName=firstName)

@app.route("/forgotPassword", methods=['GET', 'POST'])
def forgotPassword():
    loggedIn, firstName, productCountinKartForGivenUser = getLoginUserDetails()
    return render_template('404.html', loggedIn=loggedIn, firstName=firstName)


@app.route("/seeTrends", methods=['GET', 'POST'])
def seeTrends():
    trendtype = str(request.args.get('trend'))
    cur = mysql.connection.cursor()
    if (trendtype == "least"):
        cur.execute("SELECT ordered_details.productid, sum(ordered_details.quantity) AS TotalQuantity,product.product_name FROM \
                       ordered_details,product where ordered_details.productid=product.productid GROUP BY productid \
                           ORDER BY TotalQuantity ASC LIMIT 3 ")
    else:
        trendtype = "most"
        cur.execute("SELECT ordered_details.productid, sum(ordered_details.quantity) AS TotalQuantity,product.product_name FROM \
                ordered_details,product where ordered_details.productid=product.productid GROUP BY productid \
                    ORDER BY TotalQuantity DESC LIMIT 3 ")

    products = cur.fetchall()
    cur.close()
    x = []
    y = []
    for item in products:
        x.append(item['product_name'])
        y.append(item['TotalQuantity'])

    my_plot_div = plot([go.Bar(x=x, y=y)], output_type='div')

    return render_template('trends.html',
                           div_placeholder=Markup(my_plot_div), trendtype=trendtype
                           )

## Payment module implementation 

@app.route("/createOrder", methods=['GET', 'POST'])
def createOrder():
    if isUserLoggedIn():
        loggedIn, firstName, productCountinKartForGivenUser = getLoginUserDetails()
    totalsum = request.args.get('total')
    float_totalsum = round(float(request.args.get('total')),2)
    amount_payable = int(str(float_totalsum).replace(".",""))
    email, username, ordernumber, address, fullname, phonenumber = extractOrderdetails(request, totalsum)

    if amount_payable > 1500000:
        amount_payable = 1500000

    data = { "amount": amount_payable, "currency": "INR", "receipt": str(ordernumber[0]) } 
    payment = client.order.create(data=data)

    cartdetails, totalsum, tax = getusercartdetails()

    if email:
        sendEmailconfirmation(email, username, ordernumber, phonenumber)

    return render_template("pay.html", payment=payment, cartData=cartdetails, totalsum=totalsum, tax=tax,
                                productCountinKartForGivenUser=productCountinKartForGivenUser, loggedIn=loggedIn,
                               firstName=firstName)

import pandas as pd

@app.route("/paymentSuccess", methods=['POST'])
def paymentSuccess():
    time.sleep(10)
    payments = client.payment.all()
    p_df = pd.DataFrame(payments['items'])
    rzp_order_id = request.args.get('order')
    our_order_id = request.args.get('id')
    this_transaction = pd.DataFrame
    this_transaction = p_df[p_df['order_id'] == rzp_order_id]
    status = this_transaction['status']
    print(status)
    if( str(status).split()[1] == 'captured' ) :
        userId = User.query.with_entities(User.userid).filter(User.email == session['email']).first()
        addOrderedproducts(userId, our_order_id, "Payment Processed")
        removeordprodfromcart(userId)
        updateSalestransaction(our_order_id, rzp_order_id, "Success")
    else:
        addOrderedproducts(userId, our_order_id, "Payment Failed")
        updateSalestransaction(our_order_id, rzp_order_id, "Failed")

    return redirect(url_for('root'))



@app.route("/orders", methods=['GET', 'POST'])
def orders():
    loggedIn, firstName, productCountinKartForGivenUser = getLoginUserDetails()
    userId = User.query.with_entities(User.userid).filter(User.email == session['email']).first()
    orders, orderDetails = getOrderedProducts(userId)
    orderDict = {t[0]: t[1] for t in orders}

    data = []
    for od in orderDetails:
        d = {}
        product = getProductDetails(od.productid)
        d['product_name'] = product.product_name
        d['image'] = product.image
        d['description'] = product.description
        d['quantity'] = od.quantity
        d['ordered_date'] = orderDict[od.orderid]
        data.append(d)

    return render_template('orderDetails.html', loggedIn=loggedIn, firstName=firstName, details=data,
                                productCountinKartForGivenUser=productCountinKartForGivenUser)


@app.route("/createBid", methods = ["GET"])
def createBid():
    print("Create Bid")
    if isUserLoggedIn():
        userId = getUserId()
        
        # get auction Information
        api_url = loadapi['biddingEngineUrl'] + '/create_bid'
        productId = int(request.args.get('productId'))
        bidAmount = float(request.args.get('bidAmount'))
        payload = json.dumps({"productId": productId, "userId": userId, "bidAmount": bidAmount})
        print(payload)
        #response = requests.post(url = api_url, data=payload)
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", api_url, headers=headers, data=payload)
        #print(response.text)
        if 'created' in response.text.lower():
            flash('Bid Created', 'success')
        else:
            flash(str(response.text), 'danger')
         
        return redirect(url_for('productDescription', productId=productId))
    else:
        flash('please log in !!', 'success')
        return redirect(url_for('root'))
    
@app.route("/addAuctionToCart", methods=['POST'])
def addAuctionToCart():
  try:
    payload = request.get_json()
    #print(payload)
    userId = int(payload["userId"])
    productId  = int(payload["productId"])
    bidPrice = float(payload["bidPrice"])
    persistAuctionToCart(productId, userId, bidPrice)
    #print('persistAuctionToCart')
    return jsonify({"status": 200})
  except Exception as e:
    return jsonify({"status": 400, "err": str(e)})


@app.route("/bids", methods=['GET'])
def getBids():
    ' In Progress '
    try:
        # get logged in userid
        users = User.query.with_entities(User.userid).filter(User.email == session['email']).all()
        for user in users:
            userId = user['userid']
        
        # get bids Information
        api_url = loadapi['biddingEngineUrl'] + '/user_bids'
        params = {"userId": userId}
        response = requests.get(api_url, params=params)
        response_json = response.json()
        user_bids = list(response_json)
            
        
        return render_template('userBids.html', bids=user_bids)
    except Exception as e:
        return jsonify({"status": 400, "err": str(e)})
    
    

