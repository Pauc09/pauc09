package com.api.challenge.Domain.Curso;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public record CursosDTO(
        @NotBlank String nombre,
        @NotNull Categoria categoria
) {

}
