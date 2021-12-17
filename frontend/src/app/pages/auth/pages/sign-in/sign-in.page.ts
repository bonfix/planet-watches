import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {ROUTER_UTILS} from '@core/utils/router.utils';
import {AuthService} from '../../services/auth.service';
import {NgForm} from '@angular/forms';
import {API_UTILS} from "@core/utils/api.utils";
import {getStorageItem, removeStorageItem, setStorageItem, StorageItem} from "@core/utils";
import {PageMessage} from "../../../../contracts/models/page-messages";

@Component({
  templateUrl: './sign-in.page.html',
  styleUrls: ['./sign-in.page.css'],
})

export class SignInPage implements OnInit{
  path = ROUTER_UTILS.config;
  returnUrl: string;
  @ViewChild('credentialForm') credentialForm: NgForm | undefined;

    credential = {
    email: "",
    password : ""
  };
  formError = ""
  formSuccess = "";

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private authService: AuthService,
  ) {
    this.returnUrl =
      this.activatedRoute.snapshot.queryParamMap.get('returnUrl') ||
      `/${ROUTER_UTILS.config.base.home}`;
  }

  /**
   * User signin
   * @param user
   */
  signIn(user: any, form: any): void {
    this.authService.signIn(user).then((res: any) =>{
      if(res){
        if(res.success)
            this.router.navigate([this.returnUrl]);
        else
        {
          if(res.error.error_code == API_UTILS.ErrorCodes.ACCOUNT_NOT_ACTIVATED)
          {
            //save email
            setStorageItem(StorageItem.Email, user.email)
            //set msg
            let msg: PageMessage = {
              message: "Your account needs to be activated. Check activation code sent via mail.",
              success: false,
              global: false,
              pages: []
            }
            setStorageItem(StorageItem.PageMessages, msg);
            this.router.navigate(['/', this.path.auth.root,this. path.auth.verification],);
              // {message: "Your account needs to be activated. Check activation code sent via mail."});
          }
          else
          {
            this.formError = "Login failed! Incorrect email and password!";
            form.reset();
          }
        }
      }
      else
        this.formError = "Server/network error, retry again.";
    })

  }

  /**
   * Form submit
   */
  onSubmit($event: Event, f: any) {
    // console.log("FORM:"+JSON.stringify(f))
      this.formError = ""
     this.signIn(this.credential, this.credentialForm)
  }

  ngOnInit(): void {
    //get stored email, if any
    let email = getStorageItem(StorageItem.Email);
    if(email && typeof email === 'string')
      this.credential.email = email;

     //get page messages if any
    let res = removeStorageItem(StorageItem.PageMessages);
    if(res){
      let msg = res as PageMessage
      if(msg.success)
        {
          this.formSuccess = msg.message
        }
      else
        {
          this.formError = msg.message
        }
    }
  }
}
