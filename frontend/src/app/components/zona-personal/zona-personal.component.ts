import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription, finalize } from 'rxjs';
import { Fabrica, User } from '../../interfaces/interfaces';
import { UserService } from '../../services/user.service';
import { ApiService } from '../../services/api.service';
import { FabricaImpl } from '../../clases/fabrica.class';
import { FabricaService } from '../../services/fabrica.service';

@Component({
  selector: 'app-zona-personal',
  templateUrl: './zona-personal.component.html',
  styleUrl: './zona-personal.component.css'
})
export class ZonaPersonalComponent {

  userName: string = "Usuario";

  fabricas: Fabrica[] = [];

  cargando: boolean = true;

  mostrarCrearFabrica: boolean = false;

  editarFabricaForm: boolean = false;
  fabricaEditar!: Fabrica;

  constructor(private router: Router, private userService: UserService, private apiService: ApiService) { }

  ngOnInit(): void {
    let userName = sessionStorage.getItem("user");
    if (userName != null && userName !== "") {
      this.userName = userName;
    }

    this.cargarFabricas();
  }

  abrirFabrica(id: number) {
    this.router.navigate(['/fabrica', id]);
  }

  cargarFabricas() {
    console.log("Cargando todas las fabricas...");
    this.cargando = true;

    this.apiService.getAllFabricas().pipe(
      finalize(() => {
        this.cargando = false;
        console.log("Fin de cargar todas las fabricas.");
      })
    ).subscribe({
      next: (fabricas) => {
        console.log("Respuesta: ", fabricas);
        for (let fabrica of fabricas) {
          const { id, nombre, capital, beneficios } = fabrica;
          if(id != undefined && nombre != undefined && capital != undefined && beneficios != undefined) {
            this.fabricas.push(new FabricaImpl(id, nombre, 1, 0, 0, capital, beneficios));
          }
        }
      },
      error: (error) => {
        alert("Error: " + error); 
      }
    });
  }

  //Modal para crear fabricas
  abrirCrearFabrica() {
    this.mostrarCrearFabrica = true;
  }
  cerrarCrearFabrica() {
    this.mostrarCrearFabrica = false;
  }

  //EditMaquinasForm
  abrirEditFabricaForm(fabrica: Fabrica): void {
    this.fabricaEditar = fabrica;
    this.editarFabricaForm = true;
  }
  cerrarEditFabricaForm(): void {
    this.editarFabricaForm = false;
  }

  borrarFabrica(fabrica: Fabrica): void {
    if(confirm("¿Estás seguro que deseas eliminar la fábrica?")) {
      console.log("Eliminando la fabrica...");
    
      this.apiService.eliminarFabrica(fabrica.id).pipe(
        finalize(() => {
          console.log("Fin de eliminar fabrica.");
        })
      ).subscribe({
        next: (response) => {
          console.log("Respuesta: ", response);

          //Eliminamos la fabrica
          const index = this.fabricas.findIndex(t => t.id === response.id);
          if (index !== -1) {
            this.fabricas.splice(index, 1);
          }

        },
        error: (error) => {
          alert("Error: " + error); 
        }
      });
    }
  }

  cerrarSesion() {
    this.router.navigate(['/']);
  }
}
