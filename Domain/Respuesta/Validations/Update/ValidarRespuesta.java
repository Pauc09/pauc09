package com.api.challenge.Domain.Respuesta.Validations.Update;

import com.api.challenge.Domain.Respuesta.ActualizarRespuestaDTO;

public interface ValidarRespuesta {
    void validate (ActualizarRespuestaDTO data, Long respuesta);
}
