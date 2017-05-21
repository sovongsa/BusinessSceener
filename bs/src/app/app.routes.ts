
import { HomeComponent } from "app/home/home.component";
import { RouterModule, Routes } from '@angular/router';
import { MapComponent } from "app/map/map.component";
export const appRoutes: Routes = [
    {path: '' , component: HomeComponent },
    {path: 'map/:searchQuery/:searchType' , component: MapComponent },
];
