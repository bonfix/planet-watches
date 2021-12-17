import { Injectable } from '@angular/core';
import { getStorageItem, removeStorageItem, setStorageItem, StorageItem } from '@core/utils';
import { BehaviorSubject } from 'rxjs';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {environment} from "@env/environment";
import {API_UTILS} from "@core/utils/api.utils";
import {GenericModel} from "../../../contracts/models/generic-model";

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  isLoggedIn$ = new BehaviorSubject<boolean>(!!getStorageItem(StorageItem.Auth));
  public authUrl = environment.apiUrl + API_UTILS.routes.auth.root;
  private headers = new HttpHeaders({ 'Content-Type': 'application/json' });

  constructor(  private http: HttpClient,) {
  }

  /**
   * Gets logged in status
   */
  get isLoggedIn(): boolean {
    return this.isLoggedIn$.getValue();
  }

    /**
   * Gets token
   */
  get token(): any {
    return getStorageItem(StorageItem.Auth)
  }

  /**
   * Signup
   */
    signUp(user: object) {
    return new Promise((resolve, reject) =>{
      this.http.post(this.authUrl+API_UTILS.routes.auth.signUp, user, {
      headers: this.headers
    }).subscribe((res: any) =>{
      if(res.success)
       {
         resolve(res)
       }else
         resolve(res)
      },
        (error => resolve(error.error)))
    });
  }

  /**
   * accountVerification
   */
    accountVerification(user: object) {
    return new Promise((resolve, reject) =>{
      this.http.post(this.authUrl+API_UTILS.routes.auth.verification, user, {
      headers: this.headers
    }).subscribe((res: any) =>{
      resolve(res)
      },
        (error => resolve(error.error)))
    });
  }

  /**
   * Get logged in
   */
  signIn(user: object) {
    const url = this.authUrl+API_UTILS.routes.auth.signIn
    return new Promise((resolve, reject) =>{
      this.http.post(url, user, {
      headers: this.headers
    }).subscribe((res: any) =>{
      if(res.success)
       {
         setStorageItem(StorageItem.Auth, res.data.token);
         setStorageItem(StorageItem.User, res.data);
         this.isLoggedIn$.next(res.data);
         resolve(res)
       }else
         resolve(res)
      },
        (error => {
          // console.log("ERROR4: "+JSON.stringify(error.error))
          resolve(error.error)
        }))
    });
  }

    /**
   * Get logged out
   */
  signOut(): void {
    removeStorageItem(StorageItem.Auth);
    removeStorageItem(StorageItem.User);
    removeStorageItem(StorageItem.Email);
    removeStorageItem(StorageItem.Cart);
    this.isLoggedIn$.next(false);
  }
}
