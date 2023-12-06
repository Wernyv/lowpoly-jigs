Narrow-purpose add-ons for Blender

## rotate_uv_edge_to_axis
Blender AddOn:Rotate a selected edge or vertex pair to align vertically or horizontally with island

テクスチャの解像度を抑えようとすると見栄えのために斜めの線を引きたくないわけですが、かといって複数の頂点を縦横に整列させると歪みの元となります。このアドオンでは選択した辺が垂直か水平のどちらか近いほうになるようにUV島ごと回転するものです。

https://github.com/Wernyv/rotate_uv_edge_to_axis/assets/1202041/b4c45dd4-65a5-4759-920a-50325c3a4c71

## project_3d_vretex_to_face
Blender AddOn:project multiple vertices onto a face. the last three selected vertices are the projection destination surface

複数の頂点を特定の面(三角)で指定される平面上になるように移動します。最後に選んだ3点を面の指定とみなしてそれ以外の選択頂点を移動させます。移動方向はX,Y,Z各軸と指定面の法線軸方向です。最後の3点が必要なので移動する点は面・辺で選択してもよいですが最後の3点は頂点モードで選択してください。
微妙にねじれた四角形を平面に調整する用にも使えます。

https://github.com/Wernyv/rotate_uv_edge_to_axis/assets/1202041/f3dea4eb-c0bd-440b-8991-8fddebf6f229

## move_uv_vertex_to_other
Copies coordinates between two UV vertices. You can select which of the two vertices to copy from with the properties. Case: I want to match the positions, but I don't want to merge.

ローポリゴン、ローテクスチャだとUVの共用は多く、それが左右のパーツであるならばUV展開後にパーツをコピーすればよいのですが、単一パーツの左右面だとそうもいかず、という場面で使う用です。
UV頂点は選択順序を取得できないのでプロパティの選択肢は方向となりました。

## scale_uv_edge_to_actual
Scales the UV island using one edge of the UV island as a reference to its 3D size.

テクセル密度をそろえる的なことがやりたかった感じです。UVアイランドの1辺を選択して実行すると、その辺の３D上のサイズを参照し、UVアイランドごと拡縮します。プロパティの数値はUあるいはVが1.0の場合の実寸[mm]を指定するもので、例えばテクスチャサイズが1024のときプロパティ1024で実行するとテクスチャの1画素が1mmとなるようにUVアイランドがリサイズされます。テクスチャサイズが1024の時にパラメータ512で実行すると2ピクセルが1mmとなるので同じ物理サイズに書き込める密度が倍になります(占有面積も4倍になりますが)。

https://github.com/Wernyv/lowpoly-jigs/assets/1202041/cb8ddd0c-b208-430e-b7b2-43f057571c76

