package com.api.challenge.Domain.Respuesta.Validations.create;

import com.api.challenge.Domain.Respuesta.CrearRespuestaDTO;
import com.api.challenge.Domain.Respuesta.Validations.Update.ValidarRespuesta;
import jakarta.validation.ValidationException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class RespuestaTopicoValida  implements ValidarRespuesta {
    @Autowired

    private TopicoRepository repository;

    @Override
    public void validate(CrearRespuestaDTO data){
        var topicoExiste = repository.existsById(data.topicoId());
        if (!topicoExiste){
            throw new ValidationException("Este topico no existe");
        }
        var topicoAbierto = repository.findById(data.topicoId());
        if(topicoAbierto != Estado.OPEN){
            throw new ValidationException(("Este topico no e"))
        }
    }
}
