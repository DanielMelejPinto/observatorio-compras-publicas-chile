SELECT 
    "CodigoEstado",
    CASE 
        WHEN "CodigoEstado" = 12 THEN 'Recepción Conforme'
        WHEN "CodigoEstado" = 8  THEN 'Aceptada'
        WHEN "CodigoEstado" = 9  THEN 'Cancelada'
        WHEN "CodigoEstado" = 4  THEN 'Enviada al Proveedor'
        ELSE 'Otro Estado'
    END AS descripcion_estado,
    COUNT(*) AS total_ordenes
FROM ordenes_brutas
GROUP BY "CodigoEstado"
ORDER BY total_ordenes DESC;