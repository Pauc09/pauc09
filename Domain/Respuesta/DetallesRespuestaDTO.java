package com.api.challenge.Domain.Respuesta;

import java.time.LocalDateTime;

public record DetallesRespuestaDTO(
        Long id,
        String mensaje,
        LocalDateTime fechaCreacion,
        LocalDateTime ultimaActualizacion,
        Boolean solucion,
        Boolean borrado,
        Long usuarioId,
        String username,
        Long tipicoId,
        String topico
) {
    public DetallesRespuestaDTO(Respuesta respuesta){
        this(
                respuesta.getId(),
                respuesta.getMensaje(),
                respuesta.getFechaCreacion(),
                respuesta.getUltimaActualizacion(),
                respuesta.getSolucion(),
                respuesta.getBorrado(),
                respuesta.getUsuario().getId(),
                respuesta.getUsuario(),getUsuername(),
                respuesta.gerTopico(),getId(),
                respuesta.getTopico().getTitulo());
    }
}
