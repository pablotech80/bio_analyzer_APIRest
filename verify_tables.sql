-- Verificar qué tablas existen en la base de datos
-- Ver estructura completa de media_files
SELECT column_name, data_type, character_maximum_length, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'media_files'
ORDER BY ordinal_position;

-- Ver índices
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'media_files';

-- Ver foreign keys
SELECT
    tc.constraint_name,
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE tc.table_name = 'media_files' AND tc.constraint_type = 'FOREIGN KEY';