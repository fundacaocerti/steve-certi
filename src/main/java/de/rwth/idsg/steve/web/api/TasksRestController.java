/*
 * SteVe - SteckdosenVerwaltung - https://github.com/steve-community/steve
 * Copyright (C) 2024 Fundação CERTI
 * All Rights Reserved.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
package de.rwth.idsg.steve.web.api;

import de.rwth.idsg.steve.ocpp.RequestResult;
import ocpp.cp._2015._10.ChargingProfilePurposeType;
import ocpp.cs._2015._10.RegistrationStatus;
import java.util.Optional;
import de.rwth.idsg.steve.repository.dto.ChargePointSelect;
import de.rwth.idsg.steve.SteveException;
import de.rwth.idsg.steve.repository.dto.ChargingProfile;
import de.rwth.idsg.steve.service.ChargingProfileService;
import de.rwth.idsg.steve.web.api.ApiControllerAdvice.ApiErrorResponse;
import de.rwth.idsg.steve.web.dto.ChargingProfileQueryForm;
import io.swagger.annotations.ApiResponse;
import io.swagger.annotations.ApiResponses;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import de.rwth.idsg.steve.service.ChargePointHelperService;
import de.rwth.idsg.steve.ocpp.OcppTransport;
import de.rwth.idsg.steve.ocpp.OcppProtocol;
import de.rwth.idsg.steve.service.ChargePointService16_Client;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import de.rwth.idsg.steve.web.dto.ChargingProfileForm;
import org.springframework.http.ResponseEntity;
import de.rwth.idsg.steve.web.dto.ocpp.ClearChargingProfileParams;
import de.rwth.idsg.steve.web.dto.ocpp.ClearChargingProfileParamsRest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import de.rwth.idsg.steve.ocpp.CommunicationTask;

import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import java.util.HashMap;
import java.util.Map;
import javax.validation.Valid;
import java.util.List;

import java.util.ArrayList;

@Slf4j
@RestController
@RequestMapping(value = "/api/v0/task", produces = MediaType.APPLICATION_JSON_VALUE)
@RequiredArgsConstructor
public class TasksRestController {
    @Autowired
    @Qualifier("ChargePointService16_Client")
    private ChargePointService16_Client client16;
    protected ChargePointService16_Client getClient16() {
        return client16;
    }
    @ApiResponses(value = {
        @ApiResponse(code = 200, message = "OK"),
        @ApiResponse(code = 400, message = "Bad Request", response = ApiErrorResponse.class),
        @ApiResponse(code = 401, message = "Unauthorized", response = ApiErrorResponse.class),
        @ApiResponse(code = 404, message = "Not Found", response = ApiErrorResponse.class),
        @ApiResponse(code = 500, message = "Internal Server Error", response = ApiErrorResponse.class)}
    )
    @GetMapping(value ="/status/{taskId}")
    @ResponseBody
    public Map<String, Object> getTask(@PathVariable("taskId") int taskId) {
        Map<String, Object> response = new HashMap<>();
        try
        {
            CommunicationTask task = getClient16().getTask(taskId);
            Map<String, RequestResult> taskResultMap = task.getResultMap();
            String taskChargeBox = taskResultMap.keySet().iterator().next();
            RequestResult taskResults = taskResultMap.get(taskChargeBox);
            response.put("chargeBox:", taskChargeBox);
            response.put("response:", taskResults.getResponse());
            response.put("errors:",  taskResults.getErrorMessage());
            return response;
        }
        catch(SteveException e)
        {
            throw new SteveException.NotFound(String.format("Could not find taskId %d", taskId));
        }

    }

    
}
