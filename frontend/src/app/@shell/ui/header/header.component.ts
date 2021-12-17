import {ChangeDetectionStrategy, ChangeDetectorRef, Component} from '@angular/core';
import { Router } from '@angular/router';
import { ROUTER_UTILS } from '@core/utils/router.utils';
import { AuthService } from '@pages/auth/services/auth.service';
import {Observable} from "rxjs";

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class HeaderComponent {
  isLoggedIn$!: Observable<boolean>;
  _isUserLoggedIn = false
  path = ROUTER_UTILS.config;

  constructor(private router: Router, private authService: AuthService,  private changeDetectorRef: ChangeDetectorRef) {}

    ngOnInit(): void {
    this.isLoggedIn$ = this.authService.isLoggedIn$;
    this.isLoggedIn$.subscribe((newVal)=>{
      this.loggedInValue = newVal;
      this.changeDetectorRef.detectChanges();
    });
    }

  onClickSignOut(): void {
    this.authService.signOut();

    // const { root, signIn } = ROUTER_UTILS.config.auth;
    // const { home } = ROUTER_UTILS.config.base;
    this.router.navigate(['/']);
  }
  get loggedInValue(){
    return this._isUserLoggedIn
  }
  set loggedInValue(val: boolean){
    this._isUserLoggedIn = val
  }
}
