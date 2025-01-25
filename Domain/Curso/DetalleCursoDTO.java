package com.api.challenge.Domain.Curso;

public record  DetalleCursoDTO(
        Long id,
        String nombre,
        Categoria categoria,
        Boolean activo
) {
    public DetalleCursoDTO(Curso curso){
        this(
                curso.getId(),
                curso.getNombre(),
                curso.getCategoria(),
                curso.getActivo()
        );
    }
}
