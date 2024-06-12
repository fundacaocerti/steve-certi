/*
 * SteVe - SteckdosenVerwaltung - https://github.com/steve-community/steve
 * Copyright (C) 2013-2024 SteVe Community Team
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

import de.rwth.idsg.steve.repository.TransactionRepository;
import de.rwth.idsg.steve.repository.dto.Transaction;
import de.rwth.idsg.steve.web.api.ApiControllerAdvice.ApiErrorResponse;
import de.rwth.idsg.steve.web.api.exception.BadRequestException;
import de.rwth.idsg.steve.web.dto.TransactionQueryForm;
import io.swagger.annotations.ApiResponse;
import de.rwth.idsg.steve.repository.dto.TransactionDetails;
import io.swagger.annotations.ApiResponses;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import org.springframework.web.bind.annotation.PathVariable;
import java.util.Map;
import javax.validation.Valid;
import java.util.List;

import java.util.ArrayList;

import java.util.HashMap;

/**
 * @author Sevket Goekay <sevketgokay@gmail.com>
 * @since 13.09.2022
 */
@Slf4j
@RestController
@RequestMapping(value = "/api/v0/core/meterValues", produces = MediaType.APPLICATION_JSON_VALUE)
@RequiredArgsConstructor
public class MeterValuesController {

    private final TransactionRepository transactionRepository;

    @ApiResponses(value = {
        @ApiResponse(code = 200, message = "OK"),
        @ApiResponse(code = 400, message = "Bad Request", response = ApiErrorResponse.class),
        @ApiResponse(code = 401, message = "Unauthorized", response = ApiErrorResponse.class),
        @ApiResponse(code = 500, message = "Internal Server Error", response = ApiErrorResponse.class)}
    )
    @GetMapping(value ="/{chargeBoxId}")
    @ResponseBody
    public Map <String, Map<String, Object>> get(@PathVariable("chargeBoxId") String chargeBoxId) {
        Map <String, Map<String, Object>> response = new HashMap<>();
        List<Integer> transactionPks = transactionRepository.getLastConnectorTransactions(chargeBoxId);
        for (Integer transactionPk : transactionPks)
        {
            TransactionDetails details = transactionRepository.getDetails(transactionPk);    
            Map<String, Object> transactionResponse = parseTransactionDetails(details);
            String transactionId = Integer.toString(details.getTransaction().getId());
            response.put(transactionId, transactionResponse);
        }
        log.debug("Read response for query: {}", response);
        return response;
    }

    Map<String,Object> parseTransactionDetails(TransactionDetails details)
    {
        Map<String, Object> response = new HashMap<>();
        
        response.put("connectorId", details.getTransaction().getConnectorId());
        response.put("meterValue", new ArrayList<TransactionDetails.MeterValues>());
        for (TransactionDetails.MeterValues MeterValue : details.getValues()) 
        {
            ArrayList<TransactionDetails.MeterValues> meterValuesList = (ArrayList<TransactionDetails.MeterValues>) response.get("meterValue");
            meterValuesList.add(MeterValue);
        }
        return response;
    }
}