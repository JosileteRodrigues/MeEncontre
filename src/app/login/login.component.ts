import { Component, OnInit } from '@angular/core';
import {Usuario} from '../../shared/model/usuario';
import { UserService } from '../user.service';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent implements OnInit {

  constructor(private userService: UserService){
  }

  usuario = {} as Usuario;

  
  ngOnInit() {
  }

  inserirUsuario() {
    return this.userService.cadastrarUser(this.usuario)
  }
}
