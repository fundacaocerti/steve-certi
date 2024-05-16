/*******************************************************************************
 * Copyright (c) 2024 - Fundação CERTI
 * All rights reserved.
 ******************************************************************************/
package de.rwth.idsg.steve.service;
import de.rwth.idsg.steve.repository.CurrentStatusRepository;
import de.rwth.idsg.steve.repository.dto.CurrentStatus;
import de.rwth.idsg.steve.web.dto.CurrentStatusQueryForm;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import java.util.List;
@Slf4j
@Service
@RequiredArgsConstructor
public class CurrentStatusService {
    private final CurrentStatusRepository CurrentStatusRepository;
    public List<CurrentStatus.Overview> getOverview(CurrentStatusQueryForm form) {
        return CurrentStatusRepository.getOverview(form);
    }
}