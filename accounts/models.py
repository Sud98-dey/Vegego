from django.db import models

# Create your models here.
class Users(models.Model):
	user_id = models.AutoField(db_column='user_id',primary_key=True)
	username = models.CharField(max_length=25)
	email = models.EmailField(max_length=55) 
	password = models.CharField(max_length=9)
	address = models.CharField(max_length=100)
	city = models.CharField(max_length=10)
	contactno = models.CharField(max_length=12)
	role = models.CharField(max_length=12)
	gstn = models.CharField(max_length=15)
	class Meta:
		db_table = 'Users'

class Category(models.Model):
	cat_id = models.CharField(max_length=4,unique=True)
	cat_name = models.CharField(max_length=20)
	def __str__(self):
		return self.cat_name.__str__() 
	class Meta:
		db_table = 'Category'
class Product(models.Model):
	prod_id = models.AutoField(db_column='prod_id',primary_key=True)
	prod_type = models.ForeignKey(Category,on_delete=models.CASCADE)
	prod_name = models.CharField(max_length=20)
	prod_profile = models.ImageField(upload_to='pics')
	prod_price = models.FloatField()
	def __str__(self):
		return self.prod_name.__str__()
	class Meta:
		db_table = 'Product'
# Cart of orders
class Orders(models.Model):
	order_id = models.AutoField(db_column='ord_id',primary_key=True)
	prod_id = models.IntegerField()
	prod_name = models.CharField(max_length=20)	
	prod_price = models.FloatField()
	Cust_Id = models.CharField(max_length=25,null=True)
	Customer = models.CharField(max_length=25)
	prod_Qty = models.IntegerField()
	class Meta:
		db_table = 'Orders'
class Payment_Mode(models.Model):
	Payment_Mode = models.CharField(max_length=25,blank=True,null=True)
	def __str__(self):
		return self.Payment_Mode 
# Invoice of orders
class Invoice(models.Model):
	bill_id = models.AutoField(db_column='bill_id',primary_key=True)
	order_id = models.IntegerField()
	Customer = models.CharField(max_length=25)
	Cust_Id = models.CharField(max_length=25,null=True)
	Product = models.CharField(max_length=20)
	prod_Qty = models.IntegerField() 
	address = models.TextField()
	payment_mode = models.ForeignKey(Payment_Mode,on_delete=models.CASCADE)
	bill_date = models.DateTimeField(auto_now_add=True)
	is_accepted = models.BooleanField(default=False)
	class Meta:
		db_table = 'Invoice'
# Assign Order
class AssignOrder(models.Model):
	Assign_id = models.AutoField(db_column='Assign_id',primary_key=True)
	bill_id =  models.IntegerField()
	Vendor = models.CharField(max_length=25)
	order_date = models.DateTimeField(auto_now_add=True)
	class Meta:
		db_table='AssignOrder'