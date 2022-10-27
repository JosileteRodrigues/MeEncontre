import { Component, OnInit } from '@angular/core';
import { UserService } from '../user.service';
import {Local} from '../../shared/model/local';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {estados} from '../../shared/model/states';

@Component({
  selector: 'app-list',
  templateUrl: './list.component.html',
  styleUrls: ['./list.component.css']
})
export class ListComponent implements OnInit {

  constructor(private userService: UserService, private http: HttpClient) { }
  
  states = estados;
  citys;
  listCitys;
  local = {} as Local; 
  
  ngOnInit() {
  }

  takeCity(){
    let UF
    for(let state in this.states){
      if(this.local.estado === this.states[state].nome){
        UF = this.states[state].sigla;
        this.http.get<any>(`https://servicodados.ibge.gov.br/api/v1/localidades/estados/${UF}/distritos`).subscribe({
        next: data => {
            return this.citys = data
        },
        error: error => {
            console.log(error.message);
            console.error('There was an error!', error);
        }
      })
      }
    }
  };

  async localSearch(){
      await this.http.post('http://localhost:5000/listar', this.local).subscribe({
      next: data => {
        return this.listCitys = data
      },
      error: error => {
          console.log(error.message);
          console.error('There was an error!', error);
      }
    })
    console.log(this.listCitys)
  }


}