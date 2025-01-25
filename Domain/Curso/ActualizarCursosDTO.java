package com.api.challenge.Domain.Curso;

public record ActualizarCursosDTO(
        String nombre,
        Categoria categoria,
        Boolean activo
) {
}
