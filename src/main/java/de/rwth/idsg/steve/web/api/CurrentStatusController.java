/*******************************************************************************
 * Copyright (c) 2024 - Fundação CERTI
 * All rights reserved.
 ******************************************************************************/
package de.rwth.idsg.steve.web.api;
import de.rwth.idsg.steve.SteveException;
import de.rwth.idsg.steve.repository.dto.CurrentStatus;
import de.rwth.idsg.steve.service.CurrentStatusService;
import de.rwth.idsg.steve.web.api.ApiControllerAdvice.ApiErrorResponse;
import de.rwth.idsg.steve.web.dto.CurrentStatusQueryForm;
import io.swagger.annotations.ApiResponse;
import io.swagger.annotations.ApiResponses;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@Slf4j
@RestController
@RequestMapping(value = "/api/v0/core/currentStatus", produces = MediaType.APPLICATION_JSON_VALUE)
@RequiredArgsConstructor
public class CurrentStatusController {

    private final CurrentStatusService CurrentStatusService;

    @ApiResponses(value = {
        @ApiResponse(code = 200, message = "OK"),
        @ApiResponse(code = 400, message = "Bad Request", response = ApiErrorResponse.class),
        @ApiResponse(code = 401, message = "Unauthorized", response = ApiErrorResponse.class),
        @ApiResponse(code = 404, message = "Not Found", response = ApiErrorResponse.class),
        @ApiResponse(code = 500, message = "Internal Server Error", response = ApiErrorResponse.class)}
    )

    @GetMapping(value ="/{chargeBoxId}")
    @ResponseBody
    public List<CurrentStatus.Overview> get(@PathVariable("chargeBoxId") String chargeBoxId) {
        log.debug("Read request for chargeBoxId: {}", chargeBoxId);

        CurrentStatusQueryForm.ForApi params = new CurrentStatusQueryForm.ForApi();

        params.setChargeBoxId(chargeBoxId);

        List<CurrentStatus.Overview> results = CurrentStatusService.getOverview(params);

        if (results.isEmpty()) {
            throw new SteveException.NotFound("Could not find this chargeBoxId");
        }

        return results;
    }
}