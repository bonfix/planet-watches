import {Component, OnInit} from '@angular/core';
import {ThemeList, ThemeService} from '@core/services/theme';
import {ROUTER_UTILS} from '@core/utils/router.utils';
import {LoadingService} from "@core/interceptors/loading.service";
import {HomeService} from "@pages/home/services/home.service";
import {Product} from "../../contracts/models/product";
import {removeStorageItem, setStorageItem, StorageItem} from "@core/utils";
import {Cart} from "../../contracts/cart";
import {AuthService} from "@pages/auth/services/auth.service";
import {Router} from "@angular/router";
import {PageMessage} from "../../contracts/models/page-messages";

@Component({
  templateUrl: './home.page.html',
  styleUrls: ['./home.page.css'],
})
export class HomePage implements OnInit{
  path = ROUTER_UTILS.config;
  theme = ThemeList;
  cartOpen = false
  isOpen = false
  products: Product[] = []
  cart: Cart = new Cart();

  constructor(private themeService: ThemeService, public myLoaderService: LoadingService,
              public homeService:HomeService, public auth: AuthService,  private router: Router,) {}

    ngOnInit(): void {
    this.homeService.getProducts().subscribe((res)=>{
      if(res.success){
        this.products = res.data
      }
    });
    this.cart.getSavedCart();
  }

  onClickChangeTheme(theme: ThemeList): void {
    this.themeService.setTheme(theme);
  }

  toggleCart() {
    this.cartOpen = !this.cartOpen;
  }

  saveCart(){
    this.cart.saveCart();
  }

  goToLogin(){
     //set msg
      let msg: PageMessage = {
        message: "You need to login in order to checkout.",
        success: false,
        global: false,
        pages: []
      }
      setStorageItem(StorageItem.PageMessages, msg);
      this.router.navigate(['/', this.path.auth.root, this.path.auth.signIn]);
  }

  checkout() {
    if(!this.auth.isLoggedIn$)
    {
     this.goToLogin();
    }
    else{
      //send cart to the server
      this.homeService.makeOrder(this.cart).subscribe((res)=>{
      if(res.success){
        // this.products = res.data
        this.cart.clearCart();
        //show confirmation
        alert(res.data.message);
      }
      else{
           //show error
          alert('Error making your order.');

      }
    },
        (error => {
          if(error.error.status_code == 401)
            this.goToLogin();
        }));
    }
  }
}
