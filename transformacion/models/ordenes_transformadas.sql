SELECT 
    "Codigo" AS codigo,
    "Nombre" AS nombre,
    "CodigoEstado" AS codigo_estado,
    CASE 
        WHEN "CodigoEstado" = 4  THEN 'Enviada al Proveedor'
        WHEN "CodigoEstado" = 5  THEN 'En Proceso'
        WHEN "CodigoEstado" = 6  THEN 'Aceptada'
        WHEN "CodigoEstado" = 9  THEN 'Cancelada'
        WHEN "CodigoEstado" = 12 THEN 'Recepcion Conforme'
        WHEN "CodigoEstado" = 13 THEN 'Pendiente de Recepcionar'
        WHEN "CodigoEstado" = 14 THEN 'Recepcionada Parcialmente'
        WHEN "CodigoEstado" = 15 THEN 'Recepcion Conforme Incompleta'
        ELSE 'Otro Estado'
    END AS descripcion_estado
FROM public.ordenes_brutas
