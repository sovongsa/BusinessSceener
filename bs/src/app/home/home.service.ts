import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import { environment } from 'environments/environment';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/do';

@Injectable()
export class HomeService {
  headers: Headers;
  constructor(private http: Http) {
    this.http = http;
    this.headers = new Headers();
    this.headers.append('Content-Type', 'application/json');
    this.headers.append('Access-Control-Allow-Origin', '*');
  }

  getAllCategories(): Observable<any> {
    const categoriesUrl = `${environment.API_ENDPOINT_BLUEMIX}/categories`;
    console.log(categoriesUrl, this.headers);
    return this.http.get(categoriesUrl)
      .map((response: Response) => <any>response.json());
  };



}
