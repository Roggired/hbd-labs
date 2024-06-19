package hbd.service.domain.repository

import hbd.service.domain.entity.OrderEntity
import org.springframework.data.jpa.repository.JpaRepository
import java.util.*

interface OrderRepository: JpaRepository<OrderEntity, UUID>