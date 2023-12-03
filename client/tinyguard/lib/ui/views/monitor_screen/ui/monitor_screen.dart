import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_mjpeg/flutter_mjpeg.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get_it/get_it.dart';
import 'package:tinyguard/const/app_colors.dart';
import 'package:tinyguard/data/repository/device_repository.dart';
import 'package:tinyguard/flavor_config.dart';
import 'package:tinyguard/ui/views/base/base_view.dart';
import 'package:tinyguard/view_models/monitor_view_model.dart';
import 'package:tinyguard/widget/bounding_box.dart';
import 'package:tinyguard/widget/ui_button_transparent.dart';
import '../../../../service/esp32_cam.dart';
import '../../../../widget/container.dart';

class MonitorScreen extends StatefulWidget {
  Device? device;
  MonitorScreen({
    super.key,
  });

  @override
  State<MonitorScreen> createState() => _MonitorScreenState();
}

class _MonitorScreenState extends State<MonitorScreen> {
  bool isExpanded = false;
  late MonitorViewModel viewModel;

  @override
  void initState() {
    WidgetsFlutterBinding.ensureInitialized();
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.landscapeLeft,
      DeviceOrientation.landscapeRight, // Allow landscape right orientation
    ]);
    viewModel = GetIt.instance.get<MonitorViewModel>();
    try {
      widget.device = viewModel.userRepository.user == null
          ? null
          : viewModel.userRepository.user!.devices.first;
    } catch (e) {}

    super.initState();
  }

  @override
  void dispose() {
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
    ]);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    @override
    final videoService =
        ComponentContainer().get(Component.esp32Camera) as Esp32Camera;
    return BaseView(
      viewModel: viewModel,
      mobileBuilder: (context) {
        return GestureDetector(
          onTap: () => FocusManager.instance.primaryFocus?.unfocus(),
          child: Stack(
            children: [
              Container(
                alignment: Alignment.center,
                child: Mjpeg(
                  width: MediaQuery.of(context).size.width,
                  fit: BoxFit.fitWidth,
                  stream:
                      'https://b39eaf649798009aac305a996ef7e516.serveo.net/api/device/test/image_stream',
                  isLive: true,
                  error: ((contet, error, stack) => ElevatedButton(
                      onPressed: () {
                        setState(() {});
                      },
                      child: Text('Reload'))),
                ),
              ),
              if (widget.device != null)
                StreamBuilder(
                    stream: widget.device!.image_predicts.stream,
                    builder: (context, predict) {
                      debugPrint("Stream rebuild");
                      return predict.hasData
                          ? Stack(
                              children: predict.data!.bboxes
                                  .map(
                                    (box) => BoundingBox(
                                      x: box.x,
                                      y: box.y,
                                      height: box.h,
                                      width: box.w,
                                      isCrying: box.label == 0,
                                      confidence: box.confidence,
                                    ),
                                  )
                                  .toList(),
                            )
                          : const SizedBox.shrink();
                    }),
              AnimatedPositioned(
                top: 0,
                left: MediaQuery.of(context).size.width / 2.3,
                duration: Duration(milliseconds: 200),
                child: GestureDetector(
                  child: Container(
                    padding: EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                    decoration: BoxDecoration(
                        color: Colors.white.withOpacity(0.8),
                        borderRadius: BorderRadius.only(
                            bottomLeft: Radius.circular(20),
                            bottomRight: Radius.circular(20)),
                        border: Border.all(width: 1, color: Colors.white)),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Container(
                          child: Row(
                            children: [
                              Icon(
                                Icons.spatial_audio_sharp,
                                color: AppColors.lightPurple,
                              ),
                              if (widget.device != null)
                                Row(
                                  children: [
                                    SizedBox(
                                      width: 20.w,
                                    ),
                                    StreamBuilder(
                                      stream:
                                          widget.device!.audio_streams.stream,
                                      builder: (context, predict) {
                                        return predict.hasData
                                            ? Text(
                                                predict.data!.prediction,
                                                style: TextStyle(
                                                    fontSize: 18,
                                                    color: Colors.black54,
                                                    fontWeight:
                                                        FontWeight.bold),
                                              )
                                            : const SizedBox.shrink();
                                      },
                                    ),
                                  ],
                                )
                            ],
                          ),
                        ),
                        Container(
                          height: 20,
                          padding: EdgeInsets.symmetric(horizontal: 1),
                          margin: EdgeInsets.symmetric(horizontal: 10),
                          color: AppColors.lightPurple,
                        ),
                        Container(
                          child: Row(
                            children: [
                              Icon(
                                Icons.warning,
                                color: AppColors.lightPurple,
                              ),
                            ],
                          ),
                        )
                      ],
                    ),
                  ),
                ),
              ),
              Builder(builder: (context) {
                final isExpanded = context
                    .select<MonitorViewModel, bool>((vm) => vm.isExpanding);
                return Stack(
                  children: [
                    AnimatedPositioned(
                      bottom: 20.0,
                      left: 20.0,
                      duration: Duration(milliseconds: 200),
                      child: UIButtonTransparent(
                        icon: isExpanded
                            ? Icons.chevron_right
                            : Icons.chevron_left,
                        onTap: () {
                          viewModel.setExpand();
                        },
                      ),
                    ),
                    AnimatedPositioned(
                      bottom: 20.0,
                      left: isExpanded ? 20 : 80.0,
                      duration: Duration(milliseconds: 200),
                      child: isExpanded
                          ? SizedBox.shrink()
                          : UIButtonTransparent(
                              icon: Icons.lock,
                              onTap: () {
                                viewModel.setExpand();
                              },
                            ),
                    ),
                    AnimatedPositioned(
                      bottom: 20.0,
                      left: isExpanded ? 20 : 140.0,
                      duration: Duration(milliseconds: 200),
                      child: isExpanded
                          ? SizedBox.shrink()
                          : UIButtonTransparent(
                              icon: Icons.volume_off,
                              onTap: () {},
                            ),
                    ),
                    AnimatedPositioned(
                      bottom: 20.0,
                      left: isExpanded ? 20 : 200.0,
                      duration: Duration(milliseconds: 200),
                      child: isExpanded
                          ? SizedBox.shrink()
                          : UIButtonTransparent(
                              icon: Icons.camera_outlined,
                              onTap: () {
                                viewModel.setExpand();
                              },
                            ),
                    ),
                    AnimatedPositioned(
                      top: isExpanded ? 200 : 320,
                      right: 20,
                      duration: Duration(milliseconds: 200),
                      child: isExpanded
                          ? SizedBox.shrink()
                          : UIButtonTransparent(
                              icon: Icons.mic,
                              onTap: () {
                                viewModel.setExpand();
                              },
                            ),
                    ),
                  ],
                );
              })
            ],
          ),
        );
      },
    );
  }
}
