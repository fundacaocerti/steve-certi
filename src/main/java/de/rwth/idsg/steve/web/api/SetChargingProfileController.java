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

import de.rwth.idsg.steve.ocpp.OcppTransport;
import de.rwth.idsg.steve.repository.dto.ChargingProfile;
import de.rwth.idsg.steve.repository.dto.ChargePointSelect;
import de.rwth.idsg.steve.service.ChargingProfileService;
import de.rwth.idsg.steve.service.ChargePointHelperService;
import de.rwth.idsg.steve.service.ChargePointService16_Client;
import de.rwth.idsg.steve.SteveException;
import de.rwth.idsg.steve.web.api.ApiControllerAdvice.ApiErrorResponse;
import de.rwth.idsg.steve.web.dto.ocpp.SetChargingProfileParams;
import de.rwth.idsg.steve.web.dto.ocpp.SetChargingProfileParamsRest;

import io.swagger.annotations.ApiResponse;
import io.swagger.annotations.ApiResponses;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import ocpp.cs._2015._10.RegistrationStatus;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import javax.validation.Valid;

@Slf4j
@RestController
@RequestMapping(value = "/api/v0/smartCharging/setChargingProfile", produces = MediaType.APPLICATION_JSON_VALUE)
@RequiredArgsConstructor
public class SetChargingProfileController {

    @Autowired
    private ChargePointHelperService chargePointHelperService;

    @Autowired
    @Qualifier("ChargePointService16_Client")
    private ChargePointService16_Client client16;

    private final ChargingProfileService chargingProfileService;

    @ApiResponses(value = {
        @ApiResponse(code = 200, message = "OK"),
        @ApiResponse(code = 400, message = "Bad Request", response = ApiErrorResponse.class),
        @ApiResponse(code = 401, message = "Unauthorized", response = ApiErrorResponse.class),
        @ApiResponse(code = 404, message = "Not Found", response = ApiErrorResponse.class),
        @ApiResponse(code = 500, message = "Internal Server Error", response = ApiErrorResponse.class)}
    )

    @PostMapping(value = "/{chargeBoxId}")
    @ResponseBody
    @ResponseStatus(HttpStatus.OK)
    public Map<String, Object> setChargingProfile(@PathVariable("chargeBoxId") String chargeBoxId,
           @RequestBody @Valid SetChargingProfileParamsRest setChargingProfileParamsRest) {
        if (getRegistrationStatus(chargeBoxId).isEmpty()) {
            throw new SteveException.NotFound("Could not find this chargeBoxId");
        }

        if (!isTheChargingProfileValid(setChargingProfileParamsRest.getChargingProfileId())) {
            throw new SteveException.NotFound("Could not find this chargingProfileId");
        }

        SetChargingProfileParams setChargingProfileParams = createOcpp16ParamsFromRest(chargeBoxId,
                setChargingProfileParamsRest);

        Map<String, Object> response = new HashMap<>();

        response.put("taskId", getClient16().setChargingProfile(setChargingProfileParams));

        return response;
    }

    private SetChargingProfileParams createOcpp16ParamsFromRest(
            String chargeBoxId, SetChargingProfileParamsRest params) {
        SetChargingProfileParams setChargingProfileParams = new SetChargingProfileParams();

        List<ChargePointSelect> selected = new ArrayList<ChargePointSelect>();
        selected.add(new ChargePointSelect(OcppTransport.fromValue("J"), chargeBoxId));
        setChargingProfileParams.setChargePointSelectList(selected);

        Integer chargingProfilePk = params.getChargingProfileId();
        setChargingProfileParams.setChargingProfilePk(chargingProfilePk);

        Integer connectorId = params.getConnectorId();
        setChargingProfileParams.setConnectorId(connectorId);

        return setChargingProfileParams;
    }

    private ChargePointHelperService getChargePointHelpService() {
        return chargePointHelperService;
    }

    private Optional<RegistrationStatus> getRegistrationStatus(String chargeBoxId) {
        return getChargePointHelpService().getRegistrationStatus(chargeBoxId);
    }

    private boolean isTheChargingProfileValid(Integer chargingProfilePk) {
        ChargingProfile.Details details = chargingProfileService.getDetails(chargingProfilePk);

        return details.getProfile() != null;
    }

    private ChargePointService16_Client getClient16() {
        return client16;
    }
}
