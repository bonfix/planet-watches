import {Component, ViewChild} from '@angular/core';
import {ROUTER_UTILS} from "@core/utils/router.utils";
import {ActivatedRoute, Router} from "@angular/router";
import {AuthService} from "@pages/auth/services/auth.service";
import {NgForm} from "@angular/forms";
import {setStorageItem, StorageItem} from "@core/utils";
import {PageMessage} from "../../../../contracts/models/page-messages";
import {LoadingService} from "@core/interceptors/loading.service";

@Component({
  templateUrl: './sign-up.page.html',
  styleUrls: ['./sign-up.page.css'],
})
export class SignUpPage {
    path = ROUTER_UTILS.config;
  returnUrl: string;
  @ViewChild('credentialForm') credentialForm: NgForm | undefined;

    credential = {
    email: null,
    password : null,
      passwordConf: null
    };
    formError = ""

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private authService: AuthService,
    public myLoaderService: LoadingService,
  ) {
    this.returnUrl =
      this.activatedRoute.snapshot.queryParamMap.get('returnUrl') ||
      `/${ROUTER_UTILS.config.base.home}`;
  }

    /**
   * Signup a new user
   */
    signUp(user: any, credentialForm: any): void {
    this.authService.signUp(user).then((res: any) =>{
      if(res.success)
      {
        //store user email
        setStorageItem(StorageItem.Email, user.email);
         //set msg
            let msg: PageMessage = {
              message: "Your account was created successfully. Check activation code sent via mail.",
              success: true,
              global: false,
              pages: []
            }
            setStorageItem(StorageItem.PageMessages, msg);
        this.router.navigate(['/', this.path.auth.root, this.path.auth.verification]);
        // this.router.navigate([this.returnUrl]);
      }
      else
      {
        this.formError = "An account with this email address already exists.";
      }
      credentialForm.reset();
    })

  }

  /**
   * Form submit
   */
  onSubmit($event: Event, f: any) {
      this.formError = "";
      // delete this.credential['passwordConf'];
     this.signUp(this.credential, this.credentialForm);
  }

  /**
   * Check if passwords match
   */
  passwordMatch(){
      return this.credential.password == this.credential.passwordConf;
  }
}
