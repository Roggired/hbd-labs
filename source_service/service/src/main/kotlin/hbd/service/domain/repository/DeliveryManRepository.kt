package hbd.service.domain.repository

import hbd.service.domain.entity.DeliveryManEntity
import org.springframework.data.jpa.repository.JpaRepository
import java.util.UUID

interface DeliveryManRepository: JpaRepository<DeliveryManEntity, UUID> {
}