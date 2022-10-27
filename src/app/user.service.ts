import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})

export class UserService {

  constructor(private http: HttpClient){
  }

    url: string = "http://localhost:5000/cadastrar"

  
    cadastrarUser(user){
      this.http.post('http://localhost:5000/cadastrar', user).subscribe({
      next: data => {
          console.log(user);
      },
      error: error => {
          console.log(error.message);
          console.error('There was an error!', error);
      }
    })
    }


}
