from django.shortcuts import render, redirect
from .models import Users, Book_categories, Books, cartitems, order, orderitems
from django.db.models import F
from datetime import datetime
import pytz
# Create your views here.


def index(request):
    msg = request.GET.get("msg", "")
    return render(request, 'index.html', {"msg": msg})


def forgot_password_page(request):
    msg = request.GET.get("msg", "")
    return render(request, 'forgotpassword.html', {"msg": msg})


def homepage(request):
    msg = request.GET.get("msg", "")
    categories = Book_categories.objects.all()
    books = Books.objects.filter(quantity__gt=0)
    return render(request, 'homepage.html', {"msg": msg, "categories": categories,
                                             "books": books})


def orderpage(request):
    msg = request.GET.get("msg", "")
    quantity = request.GET['q']
    price = request.GET['p']
    grand_total = request.GET['g']
    return render(request, 'orderpage.html', {
        "msg": msg,
        "quantity": quantity,
        "price": price,
        "grand_total": grand_total
    })


def placeorder(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        grand_total = request.POST.get('grand_total')
        try:
            user_id = request.session.get('id')
            cart_items = cartitems.objects.filter(user=user_id)
            user = Users.objects.get(id=user_id)
            india_timezone = pytz.timezone('Asia/Kolkata')
            current_time_in_india = datetime.now(india_timezone)
            new_order = order.objects.create(
                user=user, date=current_time_in_india, address=address, total_quantity=quantity, total_price=price, grand_total=grand_total)
            for item in cart_items:
                orderitems.objects.create(
                    order=new_order, book=item.book, quantity=item.quantity)
                Books.objects.filter(id=item.book.id).update(
                    quantity=F('quantity') - item.quantity)
                item.delete()
            return redirect('/homepage?msg=Order placed successfully')
        except Exception as e:
            print(e)
            return redirect('/cartpage?msg=Something went wrong')
    return redirect('/cartpage?msg=Please try again')


def trackorderpage(request):
    msg = request.GET.get("msg", "")
    id = request.GET.get('id')
    ord = order.objects.get(id=id)
    order_items = orderitems.objects.filter(order=id)
    return render(request, 'trackorderpage.html', {"msg": msg, 'order': ord, 'order_items': order_items})


def profile(request):
    msg = request.GET.get("msg", "")
    if request.session.get('email'):
        try:
            user_id = request.session.get('id')
            user_data = Users.objects.filter(id=user_id).first()
            return render(request, 'profile.html', {"msg": msg, 'data': user_data})
        except Users.DoesNotExist:
            return redirect('/loginpage?msg=Login again!')
    return redirect('/loginpage?msg=Something went wrong, try again!')


def update_profile(request):
    if request.POST:
        full_name = request.POST['full_name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        Users.objects.filter(email=email).update(
            full_name=full_name, phone_number=phone_number)
        return redirect('/profile?msg=Profile updated successfully')


def signuppage(request):
    msg = request.GET.get("msg", "")
    return render(request, 'signup.html', {"msg": msg})


def signup(request):
    if request.POST:
        full_name = request.POST['fullname']
        email = request.POST['email']
        phone_number = request.POST['phone']
        password = request.POST['password']
        if Users.objects.filter(email=email).exists():
            return redirect('/signuppage?msg=email already exists!')
        Users.objects.create(full_name=full_name, email=email,
                             phone_number=phone_number, password=password)
        return redirect('/loginpage?msg=You are registered successuflly!')
    return redirect('/signuppage?msg=Please signup again!')


def loginpage(request):
    msg = request.GET.get("msg", "")
    return render(request, 'loginpage.html', {"msg": msg})


def login(request):
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = Users.objects.get(email=email, password=password)
        except Users.DoesNotExist:
            return redirect('/loginpage?msg=Invalid Email or Password!')
        request.session['email'] = email
        request.session['id'] = user.id
        request.session['full_name'] = user.full_name
        return redirect('/homepage?msg=You are logged in successfully')


def logout(request):
    try:
        del request.session['email']
        del request.session['full_name']
        del request.session['id']
        return redirect('loginpage')
    except:
        return redirect('loginpage')


def setpasswordpage(request):
    msg = request.GET.get("msg", "")
    return render(request, 'setpasswordpage.html', {"msg": msg})


def confirm_email(request):
    if request.POST:
        email = request.POST['email']
        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            return redirect('/forgotpasswordpage?msg=Email does not exist!')
        return render(request, 'setpasswordpage.html', {'data': user})


def setpassword(request):
    if request.POST:
        id = request.POST['user']
        password = request.POST['password']
        try:
            user = Users.objects.get(id=id)
        except Users.DoesNotExist:
            return redirect('/forgotpasswordpage?msg=Something went wrong!')
        user.password = password
        user.save()
        return redirect('/loginpage?msg=Password changed successfully!')


def cartpage(request):
    msg = request.GET.get("msg", "")
    if request.session.get('email'):
        user_id = request.session.get('id')
        cart_items = cartitems.objects.filter(user=user_id)
        total_quantity = sum(int(item.quantity) for item in cart_items)
        total_price = sum(int(item.quantity) * int(item.book.price)
                          for item in cart_items)
        return render(request, 'cart_page.html', {
            'data': cart_items,
            'total_quantity': total_quantity,
            'total_price': total_price,
            'grand_total': total_price+55,
            'msg': msg
        })
    return redirect('/loginpage?msg=Something went wrong, try again!')


def add_to_cart(request):
    if request.session.get('email'):
        book_id = request.POST['book_id']
        user_id = request.session['id']
        user = Users.objects.get(id=user_id)
        book = Books.objects.get(id=book_id)
        cart_item = cartitems.objects.filter(user=user, book=book).first()
        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = cartitems.objects.create(user=user, book=book,
                                                 quantity=1)
        cart_item.save()
        return redirect('cartpage')
    return redirect('/loginpage?msg=Something went wrong, try again!')


def remove_from_cart(request):
    id = request.POST['cart_item_id']
    if request.session.get('email'):
        user_id = request.session.get('id')
        cart_items = cartitems.objects.get(user=user_id, id=id)
        if cart_items:
            cart_items.delete()
            return redirect('cartpage')
    return redirect('/loginpage?msg=Something went wrong, try again!')


def orderhistorypage(request):
    msg = request.GET.get("msg", "")
    user_id = request.session.get('id')
    orders = order.objects.filter(user=user_id)
    return render(request, 'orderhistorypage.html', {"msg": msg, "orders": orders})


def plus_cart(request):
    id = request.GET['id']
    cart_item = cartitems.objects.get(id=id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cartpage')


def category_filter(request):
    id = request.GET['id']
    books = Books.objects.filter(category=id)
    categories = Book_categories.objects.all()
    return render(request, 'homepage.html', {"categories": categories,
                                             "books": books})


def minus_cart(request):
    id = request.GET['id']
    cart_item = cartitems.objects.get(id=id)
    if cart_item.quantity == 1:
        cart_item.delete()
    else:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('cartpage')
