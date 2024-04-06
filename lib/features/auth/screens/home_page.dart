import 'package:flutter/material.dart';
import 'package:plantect/features/auth/screens/result_page.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final TextEditingController cropController = TextEditingController();
  final TextEditingController nitrogenController = TextEditingController();
  final TextEditingController phosphorusController = TextEditingController();
  final TextEditingController potassiumController = TextEditingController();
  final TextEditingController phController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: Container(
          height: MediaQuery.of(context).size.height,
          width: MediaQuery.of(context).size.width,
          decoration: const BoxDecoration(
            image: DecorationImage(
              image: AssetImage('assets/images/home_page.png'),
              fit: BoxFit.fill,
            ),
          ),
          child: Column(
            children: [
              SizedBox(height: MediaQuery.of(context).size.height * 0.34),
              _buildInputField(
                controller: cropController,
                hintText: 'CROP NAME',
              ),
              //SizedBox(height: MediaQuery.of(context).size.height * 0.05),
              const SizedBox(height: 45),
              _buildInputField(
                controller: nitrogenController,
                hintText: 'NITROGEN LEVEL',
              ),
              const SizedBox(height: 45),
              _buildInputField(
                controller: phosphorusController,
                hintText: 'PHOSPHORUS LEVEL',
              ),
              const SizedBox(height: 45),
              _buildInputField(
                controller: potassiumController,
                hintText: 'POTASSIUM LEVEL',
              ),
              const SizedBox(height: 45),
              _buildInputField(
                controller: phController,
                hintText: 'pH LEVEL',
              ),
              const SizedBox(height: 55),
              ElevatedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => const ResultPage(),
                    ),
                  );
                },
                style: ButtonStyle(
                  shape: MaterialStateProperty.all<RoundedRectangleBorder>(
                    RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10.0),
                    ),
                  ),
                  backgroundColor:
                      MaterialStateProperty.all(const Color(0xFFA5EFBA)),
                  minimumSize: MaterialStateProperty.all(
                    Size(MediaQuery.of(context).size.width / 1.05, 55),
                  ),
                ),
                child: const Text(
                  "VIEW RESULTS",
                  style: TextStyle(
                      color: Color(0xFF053710),
                      fontSize: 20,
                      fontWeight: FontWeight.w600),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildInputField({
    required TextEditingController controller,
    required String hintText,
  }) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 20),
      decoration: BoxDecoration(
        color: const Color(0xFFA5EFBA),
        borderRadius: BorderRadius.circular(10),
      ),
      child: TextFormField(
        controller: controller,
        decoration: InputDecoration(
          border: InputBorder.none,
          contentPadding: const EdgeInsets.all(10),
          hintText: hintText,
        ),
      ),
    );
  }
}
