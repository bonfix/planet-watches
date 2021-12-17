import {Component, OnInit, ViewChild} from '@angular/core';
import {ROUTER_UTILS} from "@core/utils/router.utils";
import {ActivatedRoute, Router} from "@angular/router";
import {AuthService} from "@pages/auth/services/auth.service";
import {NgForm} from "@angular/forms";
import {getStorageItem, removeStorageItem, setStorageItem, StorageItem} from "@core/utils";
import {PageMessage} from "../../../../contracts/models/page-messages";

@Component({
  templateUrl: './verify-user.page.html',
  styleUrls: ['./verify-user.page.css'],
})
export class VerifyUserPage implements OnInit{
    path = ROUTER_UTILS.config;
  returnUrl: string;
  @ViewChild('credentialForm') credentialForm: NgForm | undefined;

    credential = {
    email: "",
    verification_code : null
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
    this.getCachedData();
  }

  getCachedData(){
     // @ts-ignore
    this.credential.email = getStorageItem(StorageItem.Email);
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

    /**
   * verifyAccount of a new user
   */
    verifyAccount(user: any, credentialForm: any): void {
    this.authService.accountVerification(user).then((success) =>{
      if(success)
      {
        //save email
        setStorageItem(StorageItem.Email, user.email);
        //set msg
        let msg: PageMessage = {
          message: "Your account has been successfully activated. You can now login.",
          success: true,
          global: false,
          pages: []
        }
        setStorageItem(StorageItem.PageMessages, msg);
        this.router.navigate(['/', this.path.auth.root, this.path.auth.signIn]);
      }
      else
      {
        this.formError = "Account verification failed.";
      }
      credentialForm.reset();
    });

  }

  /**
   * Form submit
   */
  onSubmit($event: Event, f: any) {
      this.formError = "";
     this.verifyAccount(this.credential, this.credentialForm);
  }

  ngOnInit(): void {

  }

}
