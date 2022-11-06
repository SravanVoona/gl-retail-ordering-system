use regalia;

alter table cart add column bidprice decimal(10,0);

alter table ordered_details add column status varchar(100);

alter table sale_transaction drop column amount;
alter table sale_transaction drop column cc_number;
alter table sale_transaction drop column cc_type;
alter table sale_transaction add column razorpay_id varchar(100);
alter table product add column certificate varchar(200);

CREATE TABLE `seller` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `password` varchar(60) NOT NULL,
  `address` varchar(100) NOT NULL,
  `city` varchar(100) NOT NULL,
  `state` varchar(100) NOT NULL,
  `country` varchar(100) NOT NULL,
  `zipcode` varchar(100) NOT NULL,
  `email` varchar(120) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `PAN` varchar(20) NOT NULL,
  `UID` decimal(12,0) NOT NULL, 
  PRIMARY KEY (`id`)
);

delete from grocart.category where categoryid < 9;


insert into grocart.seller values
(201, 'BK_Retail' , 'e19d5cd5af0378da05f63f891c7467af' , 'bk_retail@gmail.com' , '371 MDR' , 'India' , 'Goa' , 'Mapusa' ,455455, 5602962331, 'HNXVH1363A' ,652201991482), 
(202, 'WU_Retail' , 'dd06000910b1e069867d91aee2b10a4c' , 'wu_retail@gmail.com' , '826 TIG' , 'India' , 'Goa' , 'Mapusa' ,455455, 5481712982, 'OJUAB0216F' ,655904597729), 
(203, 'KK_Retail' , '84a41085b40cf216a709a558b42c47b2' , 'kk_retail@gmail.com' , '912 NID' , 'India' , 'Goa' , 'Mapusa' ,455455, 4836706078, 'ZMOLF9358L' ,518617558423), 
(204, 'BA_Retail' , '6958cb94603f249b1138392aa07ce38d' , 'ba_retail@gmail.com' , '448 XIV' , 'India' , 'Goa' , 'Mapusa' ,455455, 4659255798, 'MAIVW7068E' ,553330934904), 
(205, 'FH_Retail' , 'b19fa024cb9d3e71f70127cde05186c8' , 'fh_retail@gmail.com' , '647 SSM' , 'India' , 'Goa' , 'Mapusa' ,455455, 5267152984, 'OZHSG8696P' ,410720220313), 
(206, 'IA_Retail' , '0a072b448e239a5bfada255b9c814fca' , 'ia_retail@gmail.com' , '758 QKE' , 'India' , 'Goa' , 'Mapusa' ,455455, 4681580109, 'UUBQX1465O' ,487134804985), 
(207, 'CA_Retail' , 'eca87424c08dd12a77ea2c2d5fd828cf' , 'ca_retail@gmail.com' , '675 IJJ' , 'India' , 'Goa' , 'Mapusa' ,455455, 3003303520, 'WNMZS9948J' ,459024771415), 
(208, 'YZ_Retail' , 'e84ee01c8460491e99e9eb9284433500' , 'yz_retail@gmail.com' , '893 TXU' , 'India' , 'Goa' , 'Mapusa' ,455455, 4710613244, 'UDCCJ2757A' ,735039894054), 
(209, 'FV_Retail' , 'ee2ffae77362823cae4c07a1ce254fad' , 'fv_retail@gmail.com' , '738 ICV' , 'India' , 'Goa' , 'Mapusa' ,455455, 5393674755, 'BIRMU0870Y' ,431685669997), 
(210, 'RG_Retail' , 'a12b394c1de1a48473fa1a55c1eb1ade' , 'rg_retail@gmail.com' , '226 AKT' , 'India' , 'Goa' , 'Mapusa' ,455455, 3538012003, 'BEMCC7394R' ,645063019253), 
(211, 'VA_Retail' , '2982a17f8201dc3f0cfce1ac51cb7986' , 'va_retail@gmail.com' , '087 GPF' , 'India' , 'Goa' , 'Mapusa' ,455455, 4196550349, 'NNOFZ3730E' ,464943134403), 
(212, 'LD_Retail' , '951476b63c38983430ea334ed4ce8d0a' , 'ld_retail@gmail.com' , '908 IPI' , 'India' , 'Goa' , 'Mapusa' ,455455, 3595195166, 'LVELF1444Q' ,564766850161), 
(213, 'TL_Retail' , '78cd077a4783de16e03ae87577767097' , 'tl_retail@gmail.com' , '198 BTE' , 'India' , 'Goa' , 'Mapusa' ,455455, 3187995378, 'ECYFM9017A' ,436473312295), 
(214, 'EG_Retail' , 'ec66a35888bfb2693e6de1442603607a' , 'eg_retail@gmail.com' , '215 RDK' , 'India' , 'Goa' , 'Mapusa' ,455455, 5135881211, 'IPIQK8564Q' ,771729746856), 
(215, 'UE_Retail' , '528e0689d569575637c9525d7beca346' , 'ue_retail@gmail.com' , '679 SDR' , 'India' , 'Goa' , 'Mapusa' ,455455, 5933122217, 'ZAYFQ5354R' ,643367054773), 
(216, 'XX_Retail' , 'a6170cf031d8ae7b9162ee74d9cc9bc0' , 'xx_retail@gmail.com' , '458 MCD' , 'India' , 'Goa' , 'Mapusa' ,455455, 3462148950, 'UGCCQ7273M' ,412422275115), 
(217, 'DW_Retail' , '2756ca5e3955bad784605270d3ec7884' , 'dw_retail@gmail.com' , '800 DZP' , 'India' , 'Goa' , 'Mapusa' ,455455, 5043584429, 'YJXHV1171U' ,490140057586), 
(218, 'NT_Retail' , '59e0e0539cd6956e8f62da86aae1dfb9' , 'nt_retail@gmail.com' , '949 JEU' , 'India' , 'Goa' , 'Mapusa' ,455455, 3077499252, 'UTNAP3992Q' ,675650141093), 
(219, 'LS_Retail' , '3870958080ec9b91fe58a5e88040080f' , 'ls_retail@gmail.com' , '902 XZL' , 'India' , 'Goa' , 'Mapusa' ,455455, 4087712446, 'IDXRR1830O' ,614942469407), 
(220, 'AW_Retail' , 'f0679c87535c3da1a8b8717bb10ab47a' , 'aw_retail@gmail.com' , '477 PZQ' , 'India' , 'Goa' , 'Mapusa' ,455455, 5747185675, 'PZPFM4356M' ,545923076217);

update product set brand = 'BK_Retail' where productid < 202212100;
update product set brand = 'WU_Retail' where productid < 202212300;
update product set brand = 'KK_Retail' where productid < 202212600;
update product set brand = 'BA_Retail' where productid < 202212800;
update product set brand = 'FH_Retail' where productid < 202213000;
update product set brand = 'IA_Retail' where productid < 202213200;
update product set brand = 'CA_Retail' where productid < 202214000;
update product set brand = 'YZ_Retail' where productid < 202215000;
update product set brand = 'FV_Retail' where productid < 202216000;
update product set brand = 'RG_Retail' where productid < 202217000;
update product set brand = 'VA_Retail' where productid < 202218000;
update product set brand = 'LD_Retail' where productid < 202219000;
update product set brand = 'TL_Retail' where productid < 202220000;
update product set brand = 'EG_Retail' where productid < 202221000;


update product set certificate = 'https://i.ibb.co/qdpFLzk/1.jpg' where productid <> 0;