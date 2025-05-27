from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
urlpatterns = [
    path('',views.start,name='start'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('home/',views.home,name='home'),
    path('sellerhome/',views.shome,name='shome'),
    path('buyerhome/',views.bhome,name='bhome'),
    path('adminhome/',views.adhome,name='adhome'),
    path('availablepets/',views.avail,name='avail'),
    path('contactus/',views.contact,name='contact'),
    path('adoptionprocess/',views.adopt,name='adopt'),
    path('uploadpet/',views.uploadpet,name='uploadpet'),
    path('petlist',views.mypetlist,name='mypetlist'),
    path('viewedit',views.viewedit,name='viewedit'),
    path('success_stories',views.successstories,name='successstories'),
    path('submit_story/', views.submit_story, name='submit_story'),
    path("editpet/<int:id>/", views.editpet, name="editpet"),
    path("deletepet/<int:id>/", views.deletepet, name="deletepet"),
    path("deleteuser/<int:id>/", views.deleteuser, name="deleteuser"),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('totalpetdetails/<int:id>',views.totalpetdetails,name='totalpetdetails'),
    path('search/', views.search_pets, name='search_pets'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<int:pet_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('book_pet/<int:pet_id>/', views.book_pet, name='book_pet'),
    path('buyer/orders/', views.buyer_order_history, name='buyer_order_history'),
    path('seller/orders/', views.seller_orders, name='seller_orders'),
    path('accept_request/<int:request_id>/', views.accept_request, name='accept_request'),
    path('reject_request/<int:request_id>/', views.reject_request, name='reject_request'),
    path('make_payment/<int:request_id>/', views.make_payment, name='make_payment'),
    path('orders_history/', views.order_history, name='order_history'),
    path('allpetlist',views.allpets,name='allpets'),
    path('allusers',views.allusers,name='allusers'),
    path('payment_track',views.payment_track,name='payment_track'),
    path('status_change/<int:pet_id>/', views.status_change, name='status_change'),
    path('adoption_requests',views.adoption_requests,name='adoption_requests'),
    path('cancel_order/<int:request_id>/', views.cancel_order, name='cancel_order'),
    path('add address/<int:order_id>/',views.add_address,name='add_address'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)