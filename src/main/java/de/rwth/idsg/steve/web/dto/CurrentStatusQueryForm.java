/*******************************************************************************
 * Copyright (c) 2024 - Fundação CERTI
 * All rights reserved.
 ******************************************************************************/
package de.rwth.idsg.steve.web.dto;
import io.swagger.annotations.ApiModelProperty;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
@Getter
@Setter
@ToString
public class CurrentStatusQueryForm {
    @ApiModelProperty(value = "The identifier of the transaction (i.e. charging station)")
    private String chargeBoxId;
    @ApiModelProperty(hidden = true)
    public boolean isChargeBoxIdSet() {
        return chargeBoxId != null;
    }
    @ToString(callSuper = true)
    public static class ForApi extends CurrentStatusQueryForm {
        public ForApi () {
            super();
        }
    }
}