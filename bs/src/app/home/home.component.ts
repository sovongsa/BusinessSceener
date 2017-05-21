import { FormGroup, FormControl, Validators, FormBuilder  } from '@angular/forms';
import { Component, Inject, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription } from 'rxjs/Rx';
import {HomeService} from './home.service';
import {MapService} from '../map/map.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  providers: [HomeService]
})
export class HomeComponent implements OnInit {
  names: Array<Object>;
  cognitiveAnalysisForm: FormGroup;

  constructor(private fb: FormBuilder, private homeService: HomeService, private router: Router) {

  }
ngOnInit() {
  this.cognitiveAnalysisForm = this.fb.group({
    cognitiveFormName: this.fb.group({
      name: ['', Validators.required],
      category: ['', Validators.required]
    })
  });

  this.homeService.getAllCategories()
    .subscribe(categories => {
      this.names = categories;
    });
}
  searchData(value:any) {
    this.router.navigate(['/map', value.cognitiveFormName.name, value.cognitiveFormName.category]);
  }
}
