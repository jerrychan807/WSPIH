<?php header('Content-Type: application/xml'); ?>
<menu id="file" value="File">
  <popup>
    <menuitem value="New" onclick="CreateNewDoc() />
    <menuitem value="Open" onclick="OpenDoc()" />
    <menuitem value="Close" onclick="CloseDoc()" />
  </popup>
</menu>