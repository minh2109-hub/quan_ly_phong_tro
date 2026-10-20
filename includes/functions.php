<?php
function formatMoney($n) { return number_format($n,0,",",".") . " d"; }
function formatDate($d) { if(empty($d)||$d=="0000-00-00") return "-"; return date("d/m/Y",strtotime($d)); }
function formatDateTime($d) { if(empty($d)) return "-"; return date("d/m/Y H:i",strtotime($d)); }
function e($s) { return htmlspecialchars($s??"",ENT_QUOTES,"UTF-8"); }
function setFlash($type,$message) { $_SESSION["flash"] = ["type"=>$type,"message"=>$message]; }
function getFlash() { if(isset($_SESSION["flash"])){$f=$_SESSION["flash"];unset($_SESSION["flash"]);return $f;} return null; }

function showFlash() {
    $f = getFlash();
    if(!$f) return "";
    $map = ["success"=>"check-circle","danger"=>"exclamation-circle","warning"=>"exclamation-triangle","info"=>"info-circle"];
    $icon = isset($map[$f["type"]]) ? $map[$f["type"]] : "info-circle";
    $type = htmlspecialchars($f["type"],ENT_QUOTES,"UTF-8");
    $msg  = e($f["message"]);
    return '<div class="alert alert-'.$type.' alert-dismissible fade show"><i class="fas fa-'.$icon.' me-2"></i>'.$msg.'<button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>';
}

function getStatusBadge($status) {
    $map = [
        "trong"=>'<span class="badge bg-success">Trong</span>',
        "dang_thue"=>'<span class="badge bg-primary">Dang thue</span>',
        "dang_sua_chua"=>'<span class="badge bg-warning text-dark">Dang sua chua</span>',
        "hieu_luc"=>'<span class="badge bg-success">Hieu luc</span>',
        "sap_het_han"=>'<span class="badge bg-warning text-dark">Sap het han</span>',
        "het_han"=>'<span class="badge bg-danger">Het han</span>',
        "thanh_ly"=>'<span class="badge bg-secondary">Thanh ly</span>',
        "chua_thanh_toan"=>'<span class="badge bg-warning text-dark">Chua TT</span>',
        "da_thanh_toan"=>'<span class="badge bg-success">Da TT</span>',
        "qua_han"=>'<span class="badge bg-danger">Qua han</span>',
        "moi_gui"=>'<span class="badge bg-secondary">Moi gui</span>',
        "da_tiep_nhan"=>'<span class="badge bg-info">Da tiep nhan</span>',
        "dang_xu_ly"=>'<span class="badge bg-warning text-dark">Dang xu ly</span>',
        "hoan_thanh"=>'<span class="badge bg-success">Hoan thanh</span>',
        "hoat_dong"=>'<span class="badge bg-success">Hoat dong</span>',
        "khoa"=>'<span class="badge bg-danger">Bi khoa</span>',
        "da_roi"=>'<span class="badge bg-secondary">Da roi</span>',
        "thap"=>'<span class="badge bg-success">Thap</span>',
        "trung_binh"=>'<span class="badge bg-info">Trung binh</span>',
        "cao"=>'<span class="badge bg-warning text-dark">Cao</span>',
        "khan_cap"=>'<span class="badge bg-danger">Khan cap</span>',
        "tam_ngung"=>'<span class="badge bg-secondary">Tam ngung</span>',
    ];
    return isset($map[$status]) ? $map[$status] : '<span class="badge bg-secondary">'.e($status).'</span>';
}

function paginate($total, $current, $per=10) {
    $pages = $per > 0 ? ceil($total/$per) : 1;
    return ["total"=>$total,"per_page"=>$per,"current_page"=>$current,"total_pages"=>$pages,"offset"=>($current-1)*$per];
}

function renderPagination($p, $url) {
    if($p["total_pages"]<=1) return "";
    $cur=$p["current_page"]; $tot=$p["total_pages"];
    $html='<nav><ul class="pagination justify-content-center mb-0">';
    $html.='<li class="page-item '.($cur<=1?"disabled":"").'"><a class="page-link" href="'.$url.'&page='.($cur-1).'">&laquo;</a></li>';
    for($i=max(1,$cur-2);$i<=min($tot,$cur+2);$i++) {
        $html.='<li class="page-item '.($i==$cur?"active":"").'"><a class="page-link" href="'.$url.'&page='.$i.'">'.$i.'</a></li>';
    }
    $html.='<li class="page-item '.($cur>=$tot?"disabled":"").'"><a class="page-link" href="'.$url.'&page='.($cur+1).'">&raquo;</a></li>';
    $html.='</ul></nav>';
    return $html;
}

function generateCode($prefix, $pdo, $table, $field) {
    $len = strlen($prefix)+1;
    $stmt = $pdo->query("SELECT MAX(CAST(SUBSTRING(`{$field}`, {$len}) AS UNSIGNED)) as mx FROM `{$table}`");
    $row = $stmt->fetch();
    return $prefix . str_pad(($row["mx"]??0)+1, 3, "0", STR_PAD_LEFT);
}

function getCurrentMonthYear() { return ["thang"=>(int)date("m"),"nam"=>(int)date("Y")]; }
?>