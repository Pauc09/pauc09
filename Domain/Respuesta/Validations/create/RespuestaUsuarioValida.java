package com.api.challenge.Domain.Respuesta.Validations.create;

import com.api.challenge.Domain.Respuesta.CrearRespuestaDTO;
import com.api.challenge.Domain.Respuesta.Validations.Update.ValidarRespuesta;
import jakarta.validation.ValidationException;
import org.springframework.beans.factory.annotation.Autowired;

public class RespuestaUsuarioValida implements ValidarRespuesta {
    @Autowired
    private UsuarioRepository repository;

    @Override
    public void validate(CrearRespuestaDTO data){
        var usuarioExiste = repository.existsById(data.usuarioId());
        if(!usuarioExiste){
            throw new ValidationException("Este usuario no existe");
        }
        var usuarioHabilitado = repository.findById(data.usuarioId());
        if(!usuarioHabilitado){
            throw new ValidationException(("Este usuario no esta habilitado"));
        }
    }
}
