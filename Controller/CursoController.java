package com.api.challenge.Controller;

import com.api.challenge.Domain.Curso.*;
import jakarta.transaction.Transactional;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.util.UriComponentsBuilder;
import com.api.challenge.Domain.Curso.ActualizarCursosDTO;


import java.util.Optional;

@RestController
@RequestMapping("/cursos")
public class CursoController {

    @Autowired
    private RepositoryCurso repository;

    // POST: Crear un nuevo curso
    @PostMapping
    @Transactional
    public ResponseEntity<DetalleCursoDTO> crearCurso(@RequestBody @Valid CursosDTO crearCursoDTO,
                                                      UriComponentsBuilder uriBuilder) {
        Curso curso = new Curso(crearCursoDTO);
        repository.save(curso);

        var uri = uriBuilder.path("/cursos/{id}").buildAndExpand(curso.getId()).toUri();
        return ResponseEntity.created(uri).body(new DetalleCursoDTO(curso));
    }

    // GET: Obtener un curso por ID
    @GetMapping("/{id}")
    public ResponseEntity<DetalleCursoDTO> obtenerCursoPorId(@PathVariable Long id) {
        Optional<Curso> curso = repository.findById(id);
        if (curso.isPresent()) {
            return ResponseEntity.ok(new DetalleCursoDTO(curso.get()));
        }
        return ResponseEntity.notFound().build();
    }

    // GET: Listar todos los cursos
    @GetMapping
    public ResponseEntity<?> listarCursos() {
        var cursos = repository.findAll().stream().map(DetalleCursoDTO::new).toList();
        return ResponseEntity.ok(cursos);
    }

    // PUT: Actualizar un curso por ID
    @PutMapping("/{id}")
    @Transactional
    public ResponseEntity<DetalleCursoDTO> actualizarCurso(@PathVariable Long id,
                                                           @RequestBody @Valid CursosDTO actualizarCursoDTO) {
        Optional<Curso> cursoOptional = repository.findById(id);
        if (cursoOptional.isPresent()) {
            Curso curso = cursoOptional.get();
            curso.actualizarCurso(new ActualizarCursosDTO("Nuevo Nombre", null, true));
            return ResponseEntity.ok(new DetalleCursoDTO(curso));
        }
        return ResponseEntity.notFound().build();
    }

    // DELETE: Eliminar un curso por ID
    @DeleteMapping("/{id}")
    @Transactional
    public ResponseEntity<?> eliminarCurso(@PathVariable Long id) {
        if (repository.existsById(id)) {
            repository.deleteById(id);
            return ResponseEntity.noContent().build();
        }
        return ResponseEntity.notFound().build();
    }
}
