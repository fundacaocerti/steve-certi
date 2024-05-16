/*******************************************************************************
 * Copyright (c) 2024 - Fundação CERTI
 * All rights reserved.
 ******************************************************************************/
package de.rwth.idsg.steve.repository.dto;
import lombok.Builder;
import lombok.Getter;
import lombok.ToString;
public final class CurrentStatus {
    @Getter
    @Builder
    @ToString
    public static final class Overview {
        private final String connectorId;
        private final String errorCode;
        private final String info;
        private final String status;
        private final String timestamp;
        private final String vendorErrorCode;
        private final String vendorId;
    }
}