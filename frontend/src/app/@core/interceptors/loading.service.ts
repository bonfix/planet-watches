import {BehaviorSubject} from "rxjs";
import {Injectable} from "@angular/core";

@Injectable({ providedIn: 'root' })
export class LoadingService {
    // A BehaviourSubject is an Observable with a default value
    public isLoading = new BehaviorSubject<boolean>(false);
    // public isLoadingSet = new BehaviorSubject<Set<string>>(new Set<string>());

    constructor() {}
}
