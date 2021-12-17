import { Injectable } from '@angular/core';
import { getStorageItem, removeStorageItem, setStorageItem, StorageItem } from '@core/utils';
import {BehaviorSubject, Observable} from 'rxjs';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {environment} from "@env/environment";
import {API_UTILS} from "@core/utils/api.utils";
import {Product} from "../../../contracts/models/product";
import {GenericResponse} from "../../../contracts/models/generic-response";
import {Cart} from "../../../contracts/cart";

@Injectable({
  providedIn: 'root',
})
export class HomeService {
  // products$ = new BehaviorSubject<any>(!!getItem(StorageItem.Products));
  public productsUrl = environment.apiUrl + API_UTILS.routes.products.root;
  private headers = new HttpHeaders({ 'Content-Type': 'application/json' });

  constructor(  private http: HttpClient,) {
  }


  /** GET products from the server */
  getProducts(): Observable<GenericResponse> {
    console.log("environment.production:"+environment.production);
    return this.http.get<GenericResponse>(this.productsUrl+API_UTILS.routes.products.products)
  }

  /** POST order products to the server */
  makeOrder(cart: Cart) {
    return this.http.post<GenericResponse>(this.productsUrl+API_UTILS.routes.products.order, cart.getProducts())
  }
}
