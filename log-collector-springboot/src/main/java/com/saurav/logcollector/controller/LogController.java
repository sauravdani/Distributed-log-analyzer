package com.saurav.logcollector.controller;

import com.saurav.logcollector.model.Log;
import com.saurav.logcollector.repository.LogRepository;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/logs")
@CrossOrigin(origins = "http://localhost:4200")
public class LogController {

    private final LogRepository repo;

    public LogController(LogRepository repo) {
        this.repo = repo;
    }

    @GetMapping
    public List<Log> getLogs() {
        return repo.findAll();
    }

    @PostMapping
    public Log postLog(@RequestBody Log log) {
        return repo.save(log);
    }
}
