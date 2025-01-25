package com.api.challenge.validation;

import com.api.challenge.Domain.Respuesta.ActualizarRespuestaDTO;
import com.api.challenge.Domain.Respuesta.Respuesta;
import com.api.challenge.Domain.Respuesta.RespuestaRepository;
import com.api.challenge.Domain.Respuesta.Validations.Update.ValidarRespuesta;
import com.api.challenge.Domain.topico.Topico.Estado;
import com.api.challenge.Domain.topico.Topico.TopicoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import javax.validation.ValidationException;

@Component
public class SolucionDuplicada implements ValidarRespuesta {

    @Autowired
    private RespuestaRepository respuestaRepository;

    @Autowired
    private TopicoRepository topicoRepository;

    @Override
    public void validate(ActualizarRespuestaDTO data, Long id) {
        if (data.solucion()) { // Comprueba si la respuesta tiene solución
            Respuesta respuesta = respuestaRepository.getReferenceById(id); // Obtener referencia de la respuesta por ID
            var topicoResuelto = topicoRepository.getReferenceById(respuesta.getTopico().getId()); // Obtener tópico relacionado

            if (topicoResuelto.getEstado() == Estado.CLOSED) { // Verifica si el tópico está cerrado
                throw new ValidationException("Este tópico ya está cerrado y no se pueden agregar nuevas soluciones.");
            }
        }
    }
}
