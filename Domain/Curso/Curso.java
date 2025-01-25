package com.api.challenge.Domain.Curso;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.EqualsAndHashCode;
import lombok.Getter;


@Getter
@AllArgsConstructor
@EqualsAndHashCode(of = "id")
@Entity
public class Curso {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY) // Generación automática del ID
    private Long id;

    private String nombre;

    @Enumerated(EnumType.STRING)
    private Categoria categoria;
    private Boolean activo;


    public Curso(CursosDTO crearCursoDTO) {
        this.nombre = crearCursoDTO.nombre();
        this.categoria = crearCursoDTO.categoria();
        this.activo = true;
    }

    public Curso() {

    }

    public void actualizarCurso(ActualizarCursosDTO actualizarCursosDTO){
        if (actualizarCursosDTO.nombre() != null){
            this.nombre = actualizarCursosDTO.nombre();
        }
       if (actualizarCursosDTO.categoria() != null){
           this.categoria = actualizarCursosDTO.categoria();
       }
        if ( actualizarCursosDTO.activo() != null){
            this.activo = actualizarCursosDTO.activo();
        }
    }

    public void elminarCurso(){this.activo = false;}
}
