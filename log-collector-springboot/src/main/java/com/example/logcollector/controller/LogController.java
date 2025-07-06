package com.yourpackage.logcollector.controller;

import com.yourpackage.logcollector.model.Log;
import com.yourpackage.logcollector.repository.LogRepository;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/logs")
@CrossOrigin(origins = "http://localhost:4200")  // allow Angular access
public class LogController {

    private final LogRepository logRepository;

    public LogController(LogRepository logRepository) {
        this.logRepository = logRepository;
    }

    @GetMapping
    public List<Log> getAllLogs() {
        return logRepository.findAll();
    }

    @PostMapping
    public Log saveLog(@RequestBody Log log) {
        return logRepository.save(log);
    }
}
