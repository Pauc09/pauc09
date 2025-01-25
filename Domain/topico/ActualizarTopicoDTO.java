package com.api.challenge.Domain.topico;

public record ActualizarTopicoDTO (
        String titulo,
        String mensaje,
        Estado estado,
        Long cursoID
){}

