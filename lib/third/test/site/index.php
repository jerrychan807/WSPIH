<!DOCTYPE html>
<html>
    <body>
        <?php
            $dirIterator = new RecursiveDirectoryIterator('.');
            $recursiveIterator = new RecursiveIteratorIterator($dirIterator);

            foreach ($recursiveIterator as $file) {
                if (!$file->isFile()) { 
                    continue;
                }

                $ext = pathinfo($file->getPathname(), PATHINFO_EXTENSION);

                if ($ext != 'php' || $file->getBasename() == 'index.php') {
                    continue;
                }

                $href = substr($file->getPathname(), 2);
                $href = str_replace('\\', '/', $href);

                echo '<a href="' . htmlentities($href) . '">' . htmlentities($href) . '</a><br>';
            }
        ?>
    </body>
</html>