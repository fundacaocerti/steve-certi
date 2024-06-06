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

import de.rwth.idsg.steve.service.ChargePointService16_Client;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import de.rwth.idsg.steve.web.dto.ChargingProfileForm;
import org.springframework.http.ResponseEntity;
import de.rwth.idsg.steve.web.dto.ocpp.ClearChargingProfileParams;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;

import java.util.HashMap;
import java.util.Map;
import javax.validation.Valid;
import java.util.List;

@Slf4j
@RestController
@RequestMapping(value = "/api/v0/smartCharging/ChargingProfile", produces = MediaType.APPLICATION_JSON_VALUE)
@RequiredArgsConstructor
public class ChargingProfileController {

    private final ChargingProfileService ChargingProfileService;

    private static final int kNoRemoval = 0;

    @ApiResponses(value = {
        @ApiResponse(code = 200, message = "OK"),
        @ApiResponse(code = 400, message = "Bad Request", response = ApiErrorResponse.class),
        @ApiResponse(code = 401, message = "Unauthorized", response = ApiErrorResponse.class),
        @ApiResponse(code = 404, message = "Not Found", response = ApiErrorResponse.class),
        @ApiResponse(code = 500, message = "Internal Server Error", response = ApiErrorResponse.class)}
    )

    @GetMapping
    @ResponseBody
    public List<ChargingProfile.Overview> get() {
        ChargingProfileQueryForm.ForApi params = new ChargingProfileQueryForm.ForApi();

        List<ChargingProfile.Overview> results = ChargingProfileService.getOverview(params);

        if (results.isEmpty()) {
            throw new SteveException.NotFound("Could not find charging profiles");
        }

        return results;
    }

    @PostMapping
    @ResponseBody
    @ResponseStatus(HttpStatus.CREATED)
    public Map<String, Integer> add(@RequestBody @Valid ChargingProfileForm params) {

        int NewChargingProfilePk = ChargingProfileService.add(params);
        Map<String, Integer> response = new HashMap<>();
        response.put("chargingProfileId", NewChargingProfilePk);

        // Return the response map
        return response;
    }

    @DeleteMapping(value ="/{chargingProfileId}")
    @ResponseBody
    public Map<String, Object> delete(@PathVariable("chargingProfileId") Integer chargingProfileId) {
        log.debug("Delete request for chargingProfilePk: {}", chargingProfileId);

        if (ChargingProfileService.delete(chargingProfileId) == kNoRemoval) {
            throw new SteveException.NotFound("Could not find this chargingProfileId");
        }

        Map<String, Object> response = new HashMap<>();

        response.put("status", "OK");

        log.debug("Delete response: {}", response);
        return response;
    }
}
