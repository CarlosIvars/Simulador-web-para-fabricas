import { Component, EventEmitter, Output } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../../../services/api.service';
import { finalize } from 'rxjs';

@Component({
  selector: 'app-register-form',
  templateUrl: './register-form.component.html',
  styleUrl: './register-form.component.css'
})
export class RegisterFormComponent {
  @Output() close = new EventEmitter();
  @Output() inicioSesion = new EventEmitter();

  cargando: boolean = false;

  username: string = "";
  name: string = "";
  surname: string = "";
  password: string = "";

  constructor(private apiService: ApiService, private router: Router) { }

  cerrarModal(): void {
    if(!this.cargando) {
     this.close.emit();
    }
  }

  iniciarSesion(): void {
    if(!this.cargando) {
      this.inicioSesion.emit();
    }
  }

  registrarUsuario(): void {
    if(!this.cargando){
      console.log("Registrando nuevo usuario...");
      this.cargando = true;

      this.apiService.registerUser(this.username, this.name, this.surname, this.password).pipe(
        finalize(() => {
          this.cargando = false; 
          console.log("Fin del registro de usuario.");
        })
      ).subscribe({
        next: (response) => {
          console.log("Respuesta: ", response);

          if(response.user != undefined) {
            sessionStorage.setItem("user", response.user);
          }
          
          this.router.navigate(['/zona-personal']);
        },
        error: (error) => {
          alert("Error: " + error);
        }
      });
    }
  }
}
