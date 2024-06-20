package hbd.service

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.context.properties.EnableConfigurationProperties
import org.springframework.boot.runApplication

@EnableConfigurationProperties
@SpringBootApplication
class ServiceApplication

fun main(args: Array<String>) {
	runApplication<ServiceApplication>(*args)
}
