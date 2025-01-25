package com.api.challenge.Domain.topico;

import com.api.challenge.Domain.Curso.Curso;
import com.api.challenge.Domain.Respuesta.Respuesta;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.List;


@Entity
@Getter
@AllArgsConstructor
public class Topico {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank
    private String titulo;

    @NotBlank
    private String mensaje;
    @Column(name = "fecha_creacion")
    private LocalDateTime fechaCreacion;

    @Column(name = "ultima_actualizacion")
    private LocalDateTime ultimaActualizacion;

   @Enumerated(EnumType.STRING)
   private Estado estado;

    @NotNull
    private Integer anio;

    @ManyToOne (fetch = FetchType.LAZY)
    @JoinColumn(name = "usuario_id")
    private Usuario usuario;

    @ManyToOne (fetch = FetchType.LAZY)
    @JoinColumn(name = "curso_id")
    private Curso curso;

    // Constructores
    public Topico() {}

    public Topico(CrearTopicoDTO crearTopicoDTO, Usuario usuario, Curso curso) {
        this.titulo = crearTopicoDTO.getTitulo(); // Obtiene el título del DTO
        this.mensaje = crearTopicoDTO.getMensaje(); // Obtiene el mensaje del DTO
        this.fechaCreacion = LocalDateTime.now(); // Establece la fecha de creación actual
        this.ultimaActualizacion = LocalDateTime.now(); // Inicializa la última actualización
        this.estado = Estado.OPEN; // Estado inicial predeterminado
        this.anio = crearTopicoDTO.getAnio(); // Obtiene el año del DTO
        this.usuario = usuario; // Usuario asociado
        this.curso = curso; // Curso asociado
    }

    // Actualizar un tópico con información adicional, incluido el curso
    public void actualizarTopicoConCurso(ActualizarTopicoDTO actualizarTopicoDTO, Curso curso) {
        if (actualizarTopicoDTO.getTitulo() != null) {
            this.titulo = actualizarTopicoDTO.getTitulo();
        }
        if (actualizarTopicoDTO.getMensaje() != null) {
            this.mensaje = actualizarTopicoDTO.getMensaje();
        }
        if (curso != null) {
            this.curso = curso;
        }
        this.ultimaActualizacion = LocalDateTime.now(); // Actualiza la última modificación
    }

    // Actualizar un tópico sin cambiar el curso
    public void actualizarTopico(ActualizarTopicoDTO actualizarTopicoDTO) {
        if (actualizarTopicoDTO.Titulo() != null) {
            this.titulo = actualizarTopicoDTO.Titulo();
        }
        if (actualizarTopicoDTO.estado() != null) {
            this.mensaje = actualizarTopicoDTO.estado();
        }
        this.ultimaActualizacion = LocalDateTime.now(); // Actualiza la última modificación
    }

    // Eliminar un tópico (marca como inactivo en lugar de borrarlo físicamente)
    public void eliminarTopico() {
        this.estado = Estado.DELETED; // Cambia el estado del tópico a inactivo
        this.ultimaActualizacion = LocalDateTime.now(); // Actualiza la última modificación
    }

    // Cambiar el estado del tópico
    public void setEstado(Estado nuevoEstado) {
        if (nuevoEstado != null) {
            this.estado = nuevoEstado;
            this.ultimaActualizacion = LocalDateTime.now(); // Actualiza la última modificación
        }
    }

}
