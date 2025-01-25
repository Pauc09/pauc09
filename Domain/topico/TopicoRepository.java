package com.api.challenge.Domain.topico;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TopicoRepository extends JpaRepository<Topico,Long> {
    Page<Topico> findAll(Pageable pageable);
    Page<Topico> findByEstadoIsNot(Estado estado, Pageable pageable);
    Boolean existsByTituloAndMensaje(String titulo, String mensaje);
    Topico findByTitulo(String titulo);
}
