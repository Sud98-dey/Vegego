from django.shortcuts import render,redirect
from django.http import HttpResponse
from accounts.models import (Users,Category,Product,Orders,Invoice,Payment_Mode,AssignOrder)
from accounts.forms import (userForm,CategoryForm,ProductForm,CreateInvoiceForm)
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as Login
from django.contrib.auth.models import User
from django.contrib import messages
from vegego import urls
import csv,io

# Create your views here.
def adminpage(request):
	return render(request,'Admin_panel.html')
def indexpage(request):
    return render(request,'index.html')
def vendorpage(request):
	return render(request,'Vendors.html')
def customerpage(request):
	return render(request,'Customer.html')	    
def aboutpage(request):
	return render(request,'about.html')
# View for data insertion of users 
def register(request):
	
	if request.method == "POST":
		username = request.POST["username"]
		email = request.POST["email"]
		pass1 = request.POST["password1"] 
		pass2 = request.POST["password2"]
		contactno = request.POST["Phno"]
		Address = request.POST["Address"]
		city = request.POST["city"]
		is_userExists = User.objects.filter(username=username).exists()
		is_emailExists = User.objects.filter(email=email).exists()
		if is_userExists and is_emailExists:
			messages.info(request,"Username amd email are already in use ")
			return redirect('register')
		elif pass1 == pass2:
			user = User.objects.create_user(username=username,email=email,password=pass1)
			data=Users(username=username,email=email,password=pass1,address=Address,city=city,contactno=contactno,gstn="None",role='gadmin')
			data.save();user.save()
			return redirect('/login')
		else:
			messages.info(request,'password not matching')
			return redirect('/register')
	return render(request,'register.html')
def login(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request,username=username,password=password)
		print(user)
		record = Users.objects.get(username=username)
		if user is not None:
			if record.role == 'gadmin':
				Login(request,user)
				return redirect('/gadmin')
			elif record.role == 'gvendor':
				Login(request,user)
				return redirect('/gvendor')
			elif record.role == 'gcustomer':
				Login(request,user)
				return redirect('/gcustomer')
		else :
			messages.error(request,"invalid credantials!!")
	context = {}		
	return render(request,'Login.html',context)
def Logout(request):
		logout(request)
		return redirect('/')	
# Shows data of Admin 	
def show_Admin(request):
	Records_list=Users.objects.all()
	return render(request,'show.html',{'Records':Records_list})
def show_Customer(request):
	Records_list=Users.objects.all()
	return render(request,'showCustomer.html',{'Records':Records_list,'User':request.user.username})
def show_Vendor(request):
	Records_list=Users.objects.all()
	return render(request,'showVendor.html',{'Records':Records_list})
def edit_User(request,user_id):
	records=Users.objects.get(user_id = user_id)
	if request.method == 'POST':
		records = Users.objects.get(user_id=user_id)
		profile_form = userForm(request.POST or None,instance=records)
		if  profile_form.is_valid():
			profile_form.save()
			print('Your profile was successfully updated!')
			if records.role == 'gadmin':
				return redirect('/show_Admin')
			elif records.role == 'gvendor':
				return redirect('/show_Vendor')
			elif records.role == 'gcustomer':
				return redirect('/show_Customer')
		else:
			print(profile_form.errors)
	else:
		profile_form = userForm(instance=records)
	return render(request,'edit_admin.html',{'form':profile_form,'records':records})
def update_Product(request,prod_id):
    record = Product.objects.get(prod_id=prod_id)
    if request.method == 'POST':
    	record = Product.objects.get(prod_id=prod_id)
    	form = ProductForm(request.POST or None,request.FILES,instance=record)
    	if  form.is_valid():
    		form.save()
    		print('Your profile was successfully updated!')
    		return redirect('/ShowProduct')
    	else:
    		print(form.errors)
    else:
        form = ProductForm(instance=record)
    return render(request, 'edit_Product.html', {'form': form,'key':record})
def delete_Product(request,prod_id):
	record = Product.objects.get(prod_id=prod_id)
	record.delete()
	return redirect('/ShowProduct')
def delete_Order(request,id):
    order = AssignOrder.objects.get(Assign_id=id)
    order.delete()
    return redirect('/showAcceptedOrders')
def deleteCart(request,id):
    cart = Orders.objects.get(order_id=id)
    cart.delete()
    return redirect('/cart')         
def delete_User(request,user_id):
	record=Users.objects.get(user_id=user_id)
	user = User.objects.get(username=record.username)
	if record.role == 'gadmin':
		user.delete();record.delete()
		return redirect('/show_Admin')
	if record.role == 'gvendor':
		user.delete();record.delete()
		return redirect('/show_Vendor')
	if record.role == 'gcustomer':
		user.delete();record.delete()
		return redirect('/show_Customer')	
def Customer_register(request):
	if request.method == "POST":
		username = request.POST["username"]
		email = request.POST["email"]
		pass1 = request.POST["password1"] 
		pass2 = request.POST["password2"]
		contactno = request.POST["Phno"]
		Address = request.POST["Address"]
		city = request.POST["city"]
		Occupation = request.POST["Occupation"]
		is_userExists = User.objects.filter(username=username).exists()
		is_emailExists = User.objects.filter(email=email).exists()
		if is_userExists and is_emailExists:
			messages.info(request,"Username amd email are already in use ")
			return redirect('customer')
		elif pass1 == pass2:
			user = User.objects.create_user(username=username,email=email,password=pass1)
			data=Users(username=username,email=email,password=pass1,address=Address,city=city,contactno=contactno,gstn=Occupation,role='gcustomer')
			data.save();user.save()
			return redirect('/login')
		else:
			messages.info(request,'password not matching')
			return redirect('/customer')
	return render(request,'Customer_Reg.html')
def Vendor_register(request):
	if request.method == "POST":
		username = request.POST["username"]
		email = request.POST["email"]
		pass1 = request.POST["password1"] 
		pass2 = request.POST["password2"]
		contactno = request.POST["Phno"]
		Address = request.POST["Address"]
		gstn = request.POST["ssn"]
		city = request.POST["city"]
		is_userExists = User.objects.filter(username=username).exists()
		is_emailExists = User.objects.filter(email=email).exists()
		if is_userExists and is_emailExists:
			messages.info(request,"Username amd email are already in use ")
			messages.info(request,"gstn is already taken by another vendor")
			return redirect('vendor')
		elif pass1 == pass2:
			user = User.objects.create_user(username=username,email=email,password=pass1)
			data=Users(username=username,email=email,password=pass1,address=Address,city=city,contactno=contactno,gstn=gstn,role='gvendor')
			data.save();user.save()
			return redirect('/login')
		else:
			messages.info(request,'password not matching')
			return redirect('/vendor')
	return render(request,'Vendor_Reg.html')
def add_category(request):
	form=CategoryForm(request.POST)
	print(request.user.username)
	print(request.user.password)
	if request.method == 'POST':
		form = CategoryForm(request.POST or None)
		if form.is_valid():
			form.save()
			return redirect('/gadmin')
		else:
			print(form.errors)
	else:
		form = CategoryForm(request.POST)
	return render(request, 'Categories.html', {'form':form })
def add_product(request):
	form=ProductForm(request.POST)
	if request.method == 'POST':
		form = ProductForm(request.POST or None,request.FILES)
		if form.is_valid():
			form.save()
			return redirect('/gadmin')
		else:
			print(form.errors)
	else:
		form = ProductForm(request.POST,request.FILES)
	return render(request,'Products.html',{'form':form })
def addBulk(request):
	if request.method == 'POST':
		f = io.TextIOWrapper(request.FILES["AddCSV"].file)
		reader = csv.DictReader(f)
		for each in reader:
			Add_Cate = Category(cat_id=each["Id"],cat_name=each["name"])
			Add_Cate.save()
	return render(request,'addBulk.html')	
def shop(request):
	Products = Product.objects.all()
	return render(request,'shop.html',{'Products':Products})	
def AddOrder(request,id):
	uname = request.user.username
	product = Product.objects.get(prod_id=id)
	pId = product.prod_id
	pPrice = product.prod_price
	product_name = product.prod_name
	Cust_Id = uname
	print(Cust_Id)
	if request. method == 'POST':
		
		Quantity = request.POST["Pqty"]
		Customer = request.POST["Cust_Name"]
		PlaceOrder = Orders(prod_id=pId,prod_name=product_name,prod_price=pPrice,prod_Qty=Quantity,Cust_Id=Cust_Id,Customer=Customer)
		PlaceOrder.save()
		return redirect('/cart')
	else :
		print("Order was not made")
	return render(request,'order.html',{'product':product,'user':uname})	
def cart(request):
	OrderList = Orders.objects.all()
	user=request.user.username
	print('Cart:',user)
	return render(request,'cart.html',{'Orders': OrderList,'user':user})
def checkout(request,id):
	order = Orders.objects.get(order_id=id)
	productLst = [order.order_id,order.prod_name,order.prod_Qty,order.Cust_Id,order.Customer]
	form = CreateInvoiceForm(request.POST)
	if request.method == 'POST':
		form = CreateInvoiceForm(request.POST)
		if form.is_valid():
			address = form.cleaned_data['address']
			payment = form.cleaned_data['payment_mode']
			Billing = Invoice(order_id=productLst[0],
				              Product=productLst[1],prod_Qty=productLst[2],
				              Cust_Id=productLst[3],Customer=productLst[4],address=address,payment_mode=payment)
			Billing.save()
			return redirect('/cart')
		else:
			print(form.errors)
	else:
		form = CreateInvoiceForm(request.POST)
	return render(request,"Invoice.html",{'form':form,'order':order})          
def payment(request):
	if request.method == 'POST':
		Payment = request.POST["paymenttype"]
		addPayment=Payment_Mode(Payment_Mode=Payment)
		addPayment.save()
		return redirect('/gadmin')
	else:
		print("Errors")
	return render(request,'Payment.html')
def recipt(request):
	Invoices = Invoice.objects.all()
	user = request.user.username
	return render(request,'Recipts.html',{'Invoices':Invoices,'user':user})
def showOrder(request):
	Invoices=Invoice.objects.all()
	return render(request,'showOrders.html',{'Invoices':Invoices})
def AcceptOrders(request,id):
	Data = Invoice.objects.get(bill_id=id)
	uname = request.user.username
	if uname is not None and Data.is_accepted == False:
		Data.is_accepted=True
		Assign = AssignOrder(bill_id=Data.bill_id,Vendor=uname)
		Assign.save()
		Data.save()
	else :
		return redirect(request,'showOrders.html')
	return redirect(request,'Vendors.html')	
def Accepted(request):
	Data=AssignOrder.objects.all()
	return render(request,'AcceptedOrders.html',{'Data':Data})
def Unaccepted(request):
	Invoices=Invoice.objects.all()
	return render(request,'UnacceptedOrders.html',{'Invoices':Invoices})     
def List_Of_Orders(request):
	Invoices=Invoice.objects.all()
	return render(request,'OrderList.html',{'Invoices':Invoices})
def SearchView(request):
	Query = request.GET['Search']
	if Query is not None:
		Invoices=Invoice.objects.filter(Product__icontains=Query)
		return render(request,'OrderList.html',{'Invoices':Invoices})
	elif Query == "":
		Invoices=Invoice.objects.all()
		return render(request,'OrderList.html',{'Invoices':Invoices})
def getInvoiceInfo(request,id):
	InvoiceObject = Invoice.objects.get(bill_id=id)
	return render(request,'InvoiceInfo.html',{'Data':InvoiceObject})
def showAcceptedOrders(request):
	user = request.user.username
	Orders = AssignOrder.objects.filter(Vendor=user)
	context = {'Data':Orders}
	return render(request,'MyOrders.html',context)
def exportCSV(request):
	Orders = AssignOrder.objects.filter(Vendor=request.user.username)
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="AcceptedOrder_List.csv"'
	writer = csv.writer(response)
	writer.writerow(['Sr.No','Bill_No','Order_Date'])
	for order in Orders:
		writer.writerow([order.Assign_id,order.bill_id,order.order_date])
	return response
	return render(request,'MyOrders.html',context={Data:Orders})
def exportOrders(request):
	OrderList = Invoice.objects.all()
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="Orders_List.csv"'
	writer = csv.writer(response)
	writer.writerow(['Bill_No','Order_No','Customer','Product','Quantity','Address','Payment'])
	for order in OrderList:
		writer.writerow([order.bill_id,order.order_id,order.Customer,order.Product,order.prod_Qty,order.address,order.payment_mode])
	return response
	return render(request,'OrderList.html',context={'Invoices':OrderList})
def ShowProduct(request):
	Products = Product.objects.all()
	return render(request,'ShowProduct.html',{'Products':Products})